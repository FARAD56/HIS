from . import views
from django.urls import path

urlpatterns = [
    path('patient-attendance/<int:profile_id>/',  views.patient_attendance, name='patient_attendance'),
    path('medical-record/<int:profile_id>/',  views.medical_record, name='medical_record'),
    path('medication/<int:profile_id>/',  views.medication, name='medication'),
]