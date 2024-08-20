from django.contrib import admin
from .models import Diagnosis, Prescription, Investigation

# Custom admin class for Diagnosis
class DiagnosisAdmin(admin.ModelAdmin):
    def patient_name(self, obj):
        return obj.patient.full_name
    def doctor_name(self, obj):
        return obj.doctor.full_name
    
    list_display = ('id','patient_name', 'doctor_name','type','diagnosis')  
    search_fields = ('patient', 'type')

class PrescriptionAdmin(admin.ModelAdmin):
    def patient_name(self, obj):
        return obj.patient.full_name
    def doctor_name(self, obj):
        return obj.doctor.full_name
    list_display = ('id','patient_name', 'doctor_name','medicine','diagnosis','date_created')  
    search_fields = ('doctor', 'medicine') 

# Custom admin class for Investigation
class InvestigationAdmin(admin.ModelAdmin):
    def patient_name(self, obj):
        return obj.patient.full_name
    def doctor_name(self, obj):
        return obj.doctor.full_name
    list_display = ('id','patient_name', 'doctor_name','investigation') 
    search_fields = ('patient', 'investigation') 

# Register your models here.
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Investigation, InvestigationAdmin)