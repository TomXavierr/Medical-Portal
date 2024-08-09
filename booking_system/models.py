from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from accounts.models import Doctor


class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    speciality = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        self.end_time = (datetime.combine(datetime.today(), self.start_time) + timedelta(minutes=45)).time()
        super().save(*args, **kwargs)