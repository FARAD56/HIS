from django.contrib import admin
from .models import BookPatient,Availability,Appointment

# Register your models here.
class AvalabilityAdmin(admin.ModelAdmin):
    # Ensure you include the custom fields in the list display if needed
    list_display = ('doctor_id', 'day', 'time', 'type')

class BookPatientAdmin(admin.ModelAdmin):
    # Ensure you include the custom fields in the list display if needed
    list_display = ('patient_id', 'temperature', 'blood_pressure', 'triage')

admin.site.register(BookPatient,BookPatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    # Ensure you include the custom fields in the list display if needed
    def time(self, obj):
        return obj.availability.time
    def day(self, obj):
        return obj.availability.day
    def patient_name(self, obj):
        return obj.patient.full_name
    def doctor_name(self, obj):
        return obj.doctor.full_name
    
    list_display = ('id','patient_name', 'doctor_name', 'google_meet_link', 'time', 'day')

admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Availability,AvalabilityAdmin)
