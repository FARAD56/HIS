from django.db import models
from users.models import CustomUser
# Create your models here.
#not migrated
class BookPatient(models.Model):
    class Triage(models.TextChoices):
        CRITICAL = "CRITICAL"
        SEVERE = "SEVERE"
        NORMAL = 'NORMAL'
    patient_id = models.CharField(max_length=20,blank=True,null=True)
    temperature = models.CharField(max_length=20,blank=True,null=True)
    blood_pressure = models.CharField(max_length=20,blank=True,null=True)
    triage = models.CharField(max_length=20,  
                                blank=True, 
                                null=True,
                                choices=Triage.choices,
                                default=Triage.NORMAL)
    comments = models.TextField(max_length=255,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'Vitals for {self.patient_id} at {self.date_created}'
    

class Availability(models.Model):
    class Type(models.TextChoices):
        In_person = 'In Person'
        Virtual = 'Virtual'
    doctor_id = models.CharField(max_length=20,blank=True,null=True)
    date = models.DateField()
    time = models.TimeField(unique=True)
    type = models.CharField(max_length=20,blank=True,null=True,choices=Type.choices)

    @property
    def day_of_week(self):
        # Using strftime to get the full weekday name
        return self.date.strftime("%A")
    
    def __str__(self):
        return f" {self.doctor_id}"

class Appointment(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.full_name} on {self.availability.date} at {self.availability.time}"