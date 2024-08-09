from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment
from accounts.models import Doctor
from blogs_app.models import Category
# from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .utils.google_calendar import create_google_calendar_event
import datetime
from django.core.exceptions import PermissionDenied

@login_required
def doctors_list(request):
    
    doctors = Doctor.objects.all()
    categories = Category.objects.all()
    return render(request, 'doctors_list.html', locals())


@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    errors = {}
    if request.method == 'POST':
        speciality = doctor.speciality
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')

        if not date:
            errors['date'] = 'Date is required.'
        if not start_time:
            errors['start_time'] = 'Start time is required.'
            
        
        if not errors:
            try:
                date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                time_obj = datetime.datetime.strptime(start_time, '%H:%M').time()

                start_datetime = datetime.datetime.combine(date_obj, time_obj)
                end_datetime = start_datetime + datetime.timedelta(minutes=45)
                
                existing_appointments = Appointment.objects.filter(
                    doctor=doctor,
                    date=date_obj,
                    start_time__lt=end_datetime.time(),  
                    end_time__gt=start_datetime.time()   
                )
                
                if existing_appointments.exists():
                    print("asffgaggsb")
                    errors['appointment'] = 'An appointment already exists for this time slot or overlaps with it. Please choose another time.'

                if not errors:
                    appointment = Appointment.objects.create(
                        patient=request.user,
                        doctor=doctor,
                        speciality=speciality,
                        date=date_obj,
                        start_time=time_obj
                    )

                    # summary = f"Appointment with Dr. {doctor.user.get_full_name()}"
                    # description = f"Speciality: {speciality}\nPatient: {request.user.get_full_name()}"
                    # start_time_iso = start_datetime.isoformat()
                    # end_time_iso = end_datetime.isoformat()
                    # attendees_emails = [request.user.email, doctor.user.email]
                    # create_google_calendar_event(summary, description, start_time_iso, end_time_iso, attendees_emails)
                    
                    return redirect('appointment_confirmation', appointment_id=appointment.id)
            except IntegrityError:
                errors['general'] = 'An error occurred while booking the appointment.'
    
    return render(request, 'booking_form.html', {'doctor': doctor, 'errors': errors})

@login_required
def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    categories = Category.objects.all()
    return render(request, 'appointment_confirmation.html', locals())

@login_required
def user_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('date', 'start_time')
    categories = Category.objects.all()
    return render(request, 'my_appointments.html', locals())

@login_required
def doctor_appointments(request):

    doctor = request.user.doctor
    categories = Category.objects.all()
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'start_time')
    return render(request, 'doctor_schedule.html', locals())

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if appointment.patient != request.user:
        raise PermissionDenied("You do not have permission to cancel this appointment.")

    if request.method == 'POST':
        appointment.delete()
        return redirect('user_appointments')  
    
    return render(request, 'cancel_confirmation.html', {'appointment': appointment})
    
    

