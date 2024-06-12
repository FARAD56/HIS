from . import views
from django.urls import path

urlpatterns = [
    path('dashboard/',  views.dashboard_view, name='dashboard'),
    path('patient-list/',  views.patient_list, name='patient_list'),
    path('patient/<int:profile_id>/',  views.patient_details, name='patient_details'),
]