from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
from users.models import ProfileModel
from appointments.models import BookPatient
from django.db.models import Q

# Create your views here.


@login_required
def dashboard_view(request):
    doctors = CustomUser.objects.filter(is_staff=True,is_superuser=False)
    context = {
        'doctors':doctors,
    }
    return render(request,'patients/dashboard.html',context)

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

