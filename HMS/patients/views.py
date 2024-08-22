from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
from users.models import ProfileModel
from appointments.models import BookPatient
from django.db.models import Q
from medicals.models import Prescription
from django.utils import timezone


# Create your views here.


@login_required
def dashboard_view(request, profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    
    # Get all doctors who have diagnosed this patient
    diagnosed_doctors = CustomUser.objects.filter(doctor_diagnosis__patient=patient).distinct()

    medications = Prescription.objects.filter(patient=patient)
    
    # Filter appointments based on availability date and time
    now = timezone.now()
    current_day = now.strftime('%A').upper()  # Converts to full uppercase weekday name
    current_time = now.time()
    appointments = patient.appointments.filter(
        availability__day__gte=current_day,
        availability__time__gte=current_time
    ).order_by('availability__day', 'availability__time')

    context = {
        'diagnosed_doctors': diagnosed_doctors,  # Use the filtered doctors
        'medications': medications,
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'patients/dashboard.html', context)


@login_required
@staff_member_required
def patient_list(request):
    # Filtering non-staff patients
    patients = CustomUser.objects.filter(is_staff=False)
    
    
    # Filtering ProfileModel based on triage and non-staff users
    critical_patients = ProfileModel.objects.filter(user__in=patients, triage='CRITICAL')
    severe_patients = ProfileModel.objects.filter(user__in=patients, triage='SEVERE')
    normal_patients = ProfileModel.objects.filter(user__in=patients, triage='NORMAL')

    context = {
        'patients': patients,
        'critical_patients': critical_patients,
        'severe_patients': severe_patients,
        'normal_patients': normal_patients,
    }
    return render(request, 'patients/patient_list.html', context)




@login_required
def patient_details(request, profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    bookings = get_object_or_404(BookPatient,patient_id=profile_id) 
    context = {
        'patient': patient,
        'bookings':bookings
        }
    return render(request, 'patients/patient.html',context)

