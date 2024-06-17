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


admin.site.register(Appointment)
admin.site.register(Availability,AvalabilityAdmin)
