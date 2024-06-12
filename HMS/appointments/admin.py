from django.contrib import admin
from .models import BookPatient,Availability,Appointment

# Register your models here.
class AvalabilityAdmin(admin.ModelAdmin):
    # Ensure you include the custom fields in the list display if needed
    list_display = ('doctor_id', 'day_of_week', 'time', 'type')

admin.site.register(BookPatient)
admin.site.register(Appointment)
admin.site.register(Availability,AvalabilityAdmin)
