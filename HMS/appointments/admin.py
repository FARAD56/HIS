from django.contrib import admin
from .models import BookPatient,Availability,Appointment
from users.models import CustomUser
# Register your models here.
class AvalabilityAdmin(admin.ModelAdmin):
    # Ensure you include the custom fields in the list display if needed
    list_display = ('doctor_id', 'day', 'time', 'type')

class BookPatientAdmin(admin.ModelAdmin):
    # Define a custom method to get the patient (CustomUser) object using the patient_id
    def patient(self, obj):
        return CustomUser.objects.get(profile_id=obj.patient_id)

    # List the fields you want to display in the admin interface, including the custom patient method
    list_display = ('patient', 'temperature', 'blood_pressure', 'triage')

    # Optionally, if you want to display a specific field from the CustomUser model, e.g., username or full name:
    def patient_name(self, obj):
        return self.patient(obj).full_name  # or any other field like obj.patient.get_full_name()

    # Update list_display to use the patient_name method if preferred
    list_display = ('patient_name', 'temperature', 'blood_pressure', 'triage')

# Register the model with the admin site
admin.site.register(BookPatient, BookPatientAdmin)

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
