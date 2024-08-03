from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.db import IntegrityError
from django.views import View
from django.contrib.auth import get_user_model
from blogs_app.models import Category, BlogPost
import re
from django.conf import settings

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('doctor_dashboard')
        else:
            return redirect('patient_dashboard')
        
    return render(request, 'landingpage.html')

def validate_signup_data(data):
    errors = {}
    required_fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'address_line1', 'city', 'state', 'pincode']

    for field in required_fields:
        if not data.get(field):
            errors[field] = 'This field is required.'
    
    email = data.get('email')
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors['email' ] = 'Enter a valid Email'

    password1 = data.get('password1')
    password2 = data.get('password2')

    if password1 != password2:
        errors['password2'] = 'Passwords do not match.'
        
    if password1:
        if len(password1) < 8:
            errors['password1'] = 'Password must be at least 8 characters long.'
        if not re.search(r'[A-Z]', password1):
            errors['password1'] = 'Password must contain at least one uppercase letter.'
        if not re.search(r'[a-z]', password1):
            errors['password1'] = 'Password must contain at least one lowercase letter.'
        if not re.search(r'[0-9]', password1):
            errors['password1'] = 'Password must contain at least one digit.'
        if not re.search(r'[\W_]', password1):
            errors['password1'] = 'Password must contain at least one special character.'

    return errors

def handle_profile_picture(user, request):
    if 'profile_picture' in request.FILES:
        profile_picture = request.FILES['profile_picture']
        user.profile_picture.save(profile_picture.name, profile_picture)
        
        
def doctor_signup_view(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('doctor_dashboard')
        else:
            return redirect('patient_dashboard')
    
    if request.method == 'POST':
        data = request.POST
        errors = validate_signup_data(data)
        
        if not errors:
            try:
                user = User.objects.create_user(
                    email=data['email'],
                    password=data['password1'],
                    username=data['username'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    address_line1=data['address_line1'],
                    city=data['city'],
                    state=data['state'],
                    pincode=data['pincode'],
                    is_doctor=True
                )
                handle_profile_picture(user, request)
                # messages.success(request, 'Doctor account created succefully')
                login(request, user)
                return redirect('doctor_dashboard')
            except IntegrityError:
                errors['email'] = 'A user with that email or username already exists.'
        return render(request, 'doctor_signup.html', {'errors': errors})
    return render(request, 'doctor_signup.html')


def patient_signup_view(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('doctor_dashboard')
        else:
            return redirect('patient_dashboard')
    
    if request.method == 'POST':
        data = request.POST
        errors = validate_signup_data(data)
        
        if not errors:
            try:
                user = User.objects.create_user(
                    email=data['email'],
                    password=data['password1'],
                    username=data['username'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    address_line1=data['address_line1'],
                    city=data['city'],
                    state=data['state'],
                    pincode=data['pincode'],
                    is_patient=True
                )
                handle_profile_picture(user, request)
                # messages.success(request, 'Patient account created succefully')
                login(request, user)
                return redirect('patient_dashboard')
            except IntegrityError:
                errors['email'] = 'A user with that email or username already exists.'
        return render(request, 'patient_signup.html', {'errors': errors})
    return render(request, 'patient_signup.html')

@never_cache
@login_required(login_url='login')
def doctor_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'user' : request.user,
        'categories': Category.objects.all(),
        'blogs': BlogPost.objects.filter(is_draft=False),
    }
    
    return render(request, 'home.html', context)

@never_cache
@login_required(login_url='login')
def patient_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'user' : request.user,
        'categories': Category.objects.all(),
        'blogs': BlogPost.objects.filter(is_draft=False),
    }
    return render(request, 'home.html', context)


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('doctor_dashboard')
        else:
            return redirect('patient_dashboard')
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        print("ssss")
        
        if user is not None:
            print("agda")
            login(request, user)
            if user.is_doctor:
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

def user_profile_view(request):
    user = request.user
    
    return render(request, 'user_profile.html', locals())

def logout_view(request):
    logout(request)
    return redirect('home')