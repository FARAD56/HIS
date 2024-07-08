from django.contrib import admin
from .models import Diagnosis, Prescription, Investigation

# Custom admin class for Diagnosis
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor','type','diagnosis')  
    search_fields = ('patient', 'type')

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor','medicine','diagnosis')  
    search_fields = ('doctor', 'medicine') 

# Custom admin class for Investigation
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor','investigation') 
    search_fields = ('patient', 'investigation') 

# Register your models here.
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Investigation, InvestigationAdmin)