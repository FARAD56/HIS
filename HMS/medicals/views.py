from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from appointments.models import BookPatient

# Create your views here.

@login_required
def patient_attendance(request,profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    bookings = get_object_or_404(BookPatient,patient_id = profile_id)
    context = {
        'patient': patient,
        'bookings':bookings
    }

    return render(request, 'medicals/patient_attendance_details.html', context)

@login_required
@staff_member_required
def medical_record(request,profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    context = {
        'patient': patient
    }

    return render(request,'medicals/medical_records.html',context)

@login_required
def medication(request,profile_id):
    return render(request,'medicals/medication.html')