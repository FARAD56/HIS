from . import views
from django.urls import path

urlpatterns = [
    path('patient-attendance/<int:profile_id>/',  views.patient_attendance, name='patient_attendance'),
    path('medical-record/<int:profile_id>/',  views.medical_record, name='medical_record'),
    path('medication/<int:profile_id>/',  views.medication, name='medication'),
    path('diagnosis/<int:profile_id>/',  views.AddDiagnosis.as_view(), name='add_diagnosis'),
    path('prescription/<int:profile_id>/',  views.AddPrescription.as_view(), name='add_prescription'),
    path('investigation/<int:profile_id>/',  views.AddInvestigation.as_view(), name='add_investigation'),
]