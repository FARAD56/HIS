from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from appointments.models import BookPatient
from django.views.generic import View
from .models import Diagnosis, Prescription, Investigation
from django.contrib import messages
from django.utils import timezone


# Create your views here.
@login_required
def patient_attendance(request, profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    # Get today's date
    today = timezone.now().date()

    # Try to get today's booking for the patient
    try:
        bookings = BookPatient.objects.filter(patient_id=profile_id, date_created__date=today).latest('date_created')
    except BookPatient.DoesNotExist:
        # If no booking is found for today, get the most recent booking
        bookings = BookPatient.objects.filter(patient_id=profile_id).latest('date_created')

    diagnosis_list = Diagnosis.objects.filter(patient=patient).order_by('-date_created')

    context = {
        'patient': patient,
        'bookings': bookings,
        'diagnosis_list': diagnosis_list,
    }

    return render(request, 'medicals/patient_attendance_details.html', context)


@login_required
def medication(request,profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    medications = Prescription.objects.filter(patient=patient)
    context = {
        'medications': medications,
        'patient': patient
    }
    return render(request,'medicals/medication.html',context)


class AddDiagnosis(View):
    template_name = 'medicals/patient_attendance_details.html'

    def get(self,request,profile_id):
        patient = get_object_or_404(CustomUser, profile_id=profile_id)
        # Get today's date
        today = timezone.now().date()

        # Try to get today's booking for the patient
        try:
            bookings = BookPatient.objects.filter(patient_id=profile_id, date_created__date=today).latest('date_created')
        except BookPatient.DoesNotExist:
            # If no booking is found for today, get the most recent booking
            bookings = BookPatient.objects.filter(patient_id=profile_id).latest('date_created') 

        diagnosis_list = Diagnosis.objects.filter(patient=patient).order_by('-date_created')

        context = {
            'diagnosis_list': diagnosis_list,
            'patient': patient,
            'bookings':bookings
        }
        return render(request, self.template_name, context)
    
    
    def post(self,request,profile_id):
        patient = get_object_or_404(CustomUser, profile_id=profile_id)

        diagnosis = request.POST.get('diagnosis')
        diagnosis_type = request.POST.get('diagnosis_type')
      
        diagnosis_obj = Diagnosis.objects.create(
            patient=patient,
            doctor=request.user,
            diagnosis=diagnosis,
            type=diagnosis_type
        )
        if diagnosis_obj:
            messages.success(request, 'Diagnosis added successfully')
        else:
            messages.error = (request,'Failed to add diagnosis')

      
        return redirect('add_diagnosis', profile_id=profile_id)

    

class AddPrescription(View):
    template_name = 'medicals/add_prescription.html'

    def get(self,request,id):
        diagnosis = get_object_or_404(Diagnosis,id=id)
        context = {
            'diagnosis': diagnosis
        }
        return render(request,self.template_name,context)

    def post(self,request,id):
        diagnosis = get_object_or_404(Diagnosis,id=id)
        medicine = request.POST.get('medicine')
        dose = request.POST.get('dose')
        duration = request.POST.get('duration')
        strength = request.POST.get('strength')
        quantity = request.POST.get('quantity')
        frequency = request.POST.get('frequency')
        instructions = request.POST.get('instructions')
        prescription_obj = Prescription.objects.create(
            patient=diagnosis.patient,
            doctor = request.user,
            diagnosis = diagnosis,
            medicine = medicine,
            dose=dose,
            duration=duration,
            strength = strength,
            quantity = quantity,
            frequency=frequency,
            instructions=instructions
        )
        if prescription_obj:
            messages.success(request, 'Prescription added successfully')
        else:
            messages.error = (request,'Failed to add Prescription')

        return redirect('patient_attendance',diagnosis.patient.profile_id)
    

class AddInvestigation(View):
    template_name = 'medicals/add_investigation.html'
    def get(self,request,id):
        diagnosis = get_object_or_404(Diagnosis,id=id)
        context = {
            'diagnosis': diagnosis
        }
        return render(request,self.template_name,context)
    
    def post(self,request,id):
        diagnosis = get_object_or_404(Diagnosis,id=id)
        referral_facility = request.POST.get('referral_facility')
        investigation = request.POST.get('investigation')
        unit = request.POST.get('unit')
        reason = request.POST.get('unit')

        invetigation_obj = Investigation.objects.create(
            patient=diagnosis.patient,
            doctor = request.user,
            referral_facility=referral_facility,
            investigation=investigation,
            diagnosis = diagnosis,
            unit=unit,
            reason = reason
        )
        if invetigation_obj:
            messages.success(request, 'Investigation added successfully')
        else:
            messages.error = (request,'Failed to add Invesstigation')


        return redirect('patient_attendance',diagnosis.patient.profile_id)
    

class MedicalRecordsView(View):
    template_name = 'medicals/medical_records_list.html'
    
    def get(self, request, profile_id):
        patient = get_object_or_404(CustomUser, profile_id=profile_id)
        diagnosis = Diagnosis.objects.filter(patient=patient)

        context = {
            'diagnosis': diagnosis,
            'patient': patient,
        }
        return render(request, self.template_name, context)
    

class SingleRecordView(View):
    template_name = 'medicals/single_record.html'
    
    def get(self, request, id):
        diagnosis = get_object_or_404(Diagnosis,id=id)

        # Get today's date
        today = timezone.now().date()

        # Try to get today's booking for the patient
        try:
            bookings = BookPatient.objects.filter(patient_id=diagnosis.patient.profile_id, date_created__date=today).latest('date_created')
        except BookPatient.DoesNotExist:
            # If no booking is found for today, get the most recent booking
            bookings = BookPatient.objects.filter(patient_id=diagnosis.patient.profile_id).latest('date_created')

        medication = Prescription.objects.filter(diagnosis=diagnosis)
        labs = Investigation.objects.filter(diagnosis=diagnosis)
        context = {
            'diagnosis': diagnosis,
            'medication': medication,
            'labs':labs,
            'bookings':bookings,
        }
        return render(request, self.template_name, context)
    

    