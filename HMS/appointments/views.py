from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import BookPatientForm,AppointmentForm
from users.models import CustomUser
from django.db.models import Q
from .models import Availability,Appointment
# Create your views here.

@login_required
def appointment_dashboard(request):
    doctors = CustomUser.objects.filter(is_staff=True,is_superuser=False)

    if request.method == 'GET':
        speciality = request.GET.get('speciality')
        print(f"Selected speciality: {speciality}")
        if speciality and speciality != 'option1':  # Assuming 'option1' is the "Select One" option
            doctors = doctors.filter(Q(profilemodel__speciality__iexact=speciality))
            print(f"Filtered doctors: {doctors}")

    context = {'doctors':doctors}
    return render(request,'appointments/appointment_dashboard.html',context)


@login_required
def book_appointment(request,profile_id):
    doctor = get_object_or_404(CustomUser, profile_id=profile_id, is_staff=True)
    availabilities = Availability.objects.filter(doctor_id=profile_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                availability = availabilities.get(doctor_id=profile_id)
                appointment = form.save(commit=False)
                appointment.availability = availability
                appointment.user = request.user
                appointment.doctor = doctor
                appointment.save()
                print(f"Appointment saved: {appointment}")
                return redirect('session_dashboard', profile_id=profile_id)
            except Availability.DoesNotExist:
                form.add_error('availability', 'Selected availability does not exist.')
                print("Selected availability does not exist.")
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = AppointmentForm()
    
    context = {
        'doctor': doctor,
        'availabilities': availabilities,
        'form': form,
    }
    return render(request, 'appointments/book_appointment.html', context)
         

#to view appointments after it has been booked
@login_required
def session_dashboard(request,profile_id):
    user = get_object_or_404(CustomUser, profile_id=profile_id)

    #if user is staff
    if request.user.is_staff:
        appointments = Appointment.objects.filter(doctor=user)
    else:
        appointments = Appointment.objects.filter(user=request.user)

    context = {
        'appointments':appointments
    }
    return render(request,'appointments/session_dashboard.html',context)


@login_required
@staff_member_required
def book_patient(request):
    if request.method == 'POST':
        book_form = BookPatientForm(request.POST)
        if book_form.is_valid():
            triage = book_form.cleaned_data.get('triage')
            patient_id = book_form.cleaned_data.get('patient_id')
            patient = CustomUser.objects.get(profile_id=patient_id)
            patient.profilemodel.triage = triage
            patient.profilemodel.save()
            book_form.save()
            return redirect('patient_list')
    else:
        book_form = BookPatientForm()
    
    context = {
        'book_form':book_form
    }
    return render(request,'patients/book_patient.html',context)