from django.contrib import admin
from .models import Diagnosis, Prescription, Investigation

# Register your models here.

admin.site.register(Diagnosis)
admin.site.register(Prescription)
admin.site.register(Investigation)