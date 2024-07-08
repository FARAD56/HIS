from . import views
from django.urls import path

urlpatterns = [
    path('patient-attendance/<int:profile_id>/',  views.patient_attendance, name='patient_attendance'),
    path('medication/<int:profile_id>/',  views.medication, name='medication'),
    path('diagnosis/<int:profile_id>/',  views.AddDiagnosis.as_view(), name='add_diagnosis'),
    path('prescription/<int:profile_id>/',  views.AddPrescription.as_view(), name='add_prescription'),
    path('investigation/<int:profile_id>/',  views.AddInvestigation.as_view(), name='add_investigation'),
    path('get_records/<int:profile_id>/',  views.MedicalRecordView.as_view(), name='get_medical_record'),
]