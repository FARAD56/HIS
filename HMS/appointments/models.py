from django.utils import timezone
from django.db import models
from users.models import CustomUser
# Create your models here.
#not migrated
class BookPatient(models.Model):
    class Triage(models.TextChoices):
        SLELECT = "SELECT"
        CRITICAL = "CRITICAL"
        SEVERE = "SEVERE"
        NORMAL = 'NORMAL'
    patient_id = models.CharField(max_length=20,blank=True,null=True)
    temperature = models.CharField(max_length=20,blank=True,null=True)
    blood_pressure = models.CharField(max_length=20,blank=True,null=True)
    triage = models.CharField(max_length=20,  
                                blank=True, 
                                null=True,
                                choices=Triage.choices)
    comments = models.TextField(max_length=255,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'Vitals for {self.patient_id} at {self.date_created}'
    

class Availability(models.Model):
    class Type(models.TextChoices):
        In_person = 'In Person'
        Virtual = 'Virtual'
    class Day(models.TextChoices):
        MONDAY = 'MONDAY'
        TUESDAY = 'TUESDAY'
        WEDNESDAY = 'WEDNESDAY'
        THURSDAY = 'THURSDAY'
        FRIDAY = 'FRIDAY'
        SATURDAY = 'SATURDAY'
        SUNDAY = 'SUNDAY'
    doctor_id = models.CharField(max_length=20,blank=True,null=True)
    day = models.CharField(max_length=20,blank=True,null=True,choices=Day.choices)
    time = models.TimeField(unique=True,blank=True,null=True)
    type = models.CharField(max_length=20,blank=True,null=True,choices=Type.choices)
    
    def __str__(self):
        return f" {self.doctor_id}"


class Appointment(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('doctor', 'availability')

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.full_name} on {self.availability.day} at {self.availability.time} for {self.patient.full_name}"

    def save(self, *args, **kwargs):
        # Custom save logic, if needed
        super().save(*args, **kwargs)