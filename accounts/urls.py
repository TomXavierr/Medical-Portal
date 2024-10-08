from django.urls import path
from .views import doctor_signup_view, login_view, patient_signup_view, logout_view, user_profile_view,signup_options

urlpatterns = [
    path('signup/doctor/', doctor_signup_view, name='doctor_signup'),
    path('signup/patient/', patient_signup_view, name='patient_signup'),
    path('login/', login_view, name='login'),
    path('signup_options/', signup_options, name='signup_options'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile_view, name='profile'),
    
]
