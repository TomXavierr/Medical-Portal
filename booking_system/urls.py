from django.urls import path
from .views import doctors_list, book_appointment, appointment_confirmation,user_appointments,doctor_appointments, cancel_appointment

urlpatterns = [
    path('doctors_list/', doctors_list, name='doctors_list'),
    path('book/<int:doctor_id>/', book_appointment, name='book_appointment'),
    path('appointment/confirmation/<int:appointment_id>/', appointment_confirmation, name='appointment_confirmation'),
    path('user-appointments/', user_appointments, name="user_appointments"),
    path('doctor-schedule/', doctor_appointments, name="doctor_appointments"),
    path('appointment/cancel/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),
]
