from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
from users.models import ProfileModel
from appointments.models import BookPatient
from django.db.models import Q
from medicals.models import Prescription,Diagnosis
from django.utils import timezone

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm
from django.db.models import Case, When, Count
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse



@login_required
def dashboard_view(request, profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    
    # Get all doctors who have diagnosed this patient
    diagnosed_doctors = CustomUser.objects.filter(doctor_diagnosis__patient=patient).distinct()

    medications = Prescription.objects.filter(patient=patient)
    
    # Get the current date and time
    now = timezone.now()
    
    
    # Future appointments (including today)
    future_appointments = patient.appointments.all().order_by('-availability__day', 'availability__time')

    
    # Delete expired todos
    expired_todos = Todo.objects.filter(user=request.user, deadline__lt=now)
    expired_todos.delete()
    
    # Retrieve remaining todos
    user_todos = Todo.objects.filter(user=request.user).order_by('deadline')

    context = {
        'diagnosed_doctors': diagnosed_doctors,
        'medications': medications,
        'patient': patient,
        'future_appointments': future_appointments,
        'user_todos': user_todos,
    }
    return render(request, 'patients/dashboard.html', context)


@login_required
@staff_member_required
def patient_list(request):
    # Get the current date (only date, not time)
    today = timezone.now().date()

    # Get all unique patient IDs
    all_patient_ids = BookPatient.objects.values_list('patient_id', flat=True).distinct()

    # Prepare a list to hold patients and their most recent bookings
    patient_bookings = []

    for patient_id in all_patient_ids:
        # Get today's booking if available
        try:
            booking = BookPatient.objects.filter(patient_id=patient_id, date_created__date=today).latest('date_created')
        except BookPatient.DoesNotExist:
            # If no booking is found for today, get the most recent booking
            booking = BookPatient.objects.filter(patient_id=patient_id).latest('date_created')
        
        # Append the booking along with the corresponding patient ID to the list
        patient_bookings.append((booking.patient_id, booking))

    # Sort the list by the booking date (most recent first)
    patient_bookings.sort(key=lambda x: x[1].date_created, reverse=True)

    # Extract sorted patient IDs
    sorted_patient_ids = [item[0] for item in patient_bookings]

    # Retrieve CustomUser objects for the sorted patient IDs, maintaining the order
    patients = CustomUser.objects.filter(profile_id__in=sorted_patient_ids).order_by(
        Case(
            *[When(profile_id=profile_id, then=pos) for pos, profile_id in enumerate(sorted_patient_ids)]
        )
    )

    # Filter patients based on their triage levels
    critical_patients = patients.filter(profilemodel__triage='CRITICAL')
    severe_patients = patients.filter(profilemodel__triage='SEVERE')
    normal_patients = patients.filter(profilemodel__triage='NORMAL')

    # Prepare the context to include patient bookings
    context = {
        'patients': patients,
        'critical_patients': critical_patients,
        'severe_patients': severe_patients,
        'normal_patients': normal_patients,
    }
    return render(request, 'patients/patient_list.html', context)



@login_required
def patient_details(request, profile_id):
    # Get the patient object or return a 404 if not found
    patient = get_object_or_404(CustomUser, profile_id=profile_id)

    # Get today's date
    today = timezone.now().date()

    # Try to get today's booking for the patient
    try:
        booking = BookPatient.objects.filter(patient_id=profile_id, date_created__date=today).latest('date_created')
    except BookPatient.DoesNotExist:
        # If no booking is found for today, get the most recent booking
        booking = BookPatient.objects.filter(patient_id=profile_id).latest('date_created')

    context = {
        'patient': patient,
        'booking': booking
    }
    return render(request, 'patients/patient.html', context)

class TodoCreateView(CreateView):
    form_class = TodoForm
    template_name = 'users/add_activity.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        profile_id = self.request.user.profile_id
        if self.request.user.is_staff:
            return reverse_lazy('doctor_dashboard', kwargs={'profile_id': profile_id})
        else:
            return reverse_lazy('dashboard', kwargs={'profile_id': profile_id})

class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm
    pk_url_kwarg = 'id'  # Specify the lookup field
    template_name = 'users/add_activity.html'

    def get_initial(self):
        # Get the current todo object
        todo = self.get_object()
        # Return the initial data for the form
        return {
            'task': todo.task,
            'deadline': todo.deadline,
        }
    
    def get_success_url(self):
        profile_id = self.request.user.profile_id
        if self.request.user.is_staff:
            return reverse_lazy('doctor_dashboard', kwargs={'profile_id': profile_id})
        else:
            return reverse_lazy('dashboard', kwargs={'profile_id': profile_id})

class TodoDeleteView(DeleteView):
    model = Todo
    #modal to confirm delete
    pk_url_kwarg = 'id'  # Specify the lookup field
    # template_name = 'users/add_activity.html'
    def get_success_url(self):
        profile_id = self.request.user.profile_id
        if self.request.user.is_staff:
            return reverse_lazy('doctor_dashboard', kwargs={'profile_id': profile_id})
        else:
            return reverse_lazy('dashboard', kwargs={'profile_id': profile_id})

class TodoCompleteView(View):
    def post(self, request, id):
        todo = get_object_or_404(Todo, pk=id, user=request.user)
        todo.is_completed = True
        todo.save()
        if todo.user.is_staff:
            return redirect('doctor_dashboard',todo.user.profile_id)
        else:
            return redirect('dashboard',todo.user.profile_id)

def get_chart_data(request):
    # Count the diagnosis of diseases
    disease_counts = Diagnosis.objects.values('diagnosis').annotate(count=Count('diagnosis'))

    # Create labels and data for the diagnosis chart
    labels = []
    data = []
    for disease_count in disease_counts:
        labels.append(disease_count['diagnosis'])
        data.append(disease_count['count'])

    diagnosis_data = {
        'labels': labels,
        'data': data
    }

    # Get the last 6 days of patient bookings including today
    six_days_ago = now().date() - timedelta(days=5)
    vitals = BookPatient.objects.filter(patient_id=request.user.profile_id, date_created__date__gte=six_days_ago).order_by('date_created')

    # Prepare vitals data for the chart
    vitals_data = {
        'labels': [],
        'temperature': [],
        'systole': [],
        'diastole': []
    }

    for booking in vitals:
        vitals_data['labels'].append(booking.date_created.strftime('%Y-%m-%d'))
        vitals_data['temperature'].append(booking.temperature)  # Replace with the actual field for temperature
        
        # Extract systole and diastole from blood pressure
        blood_pressure = booking.blood_pressure  # Replace with the actual field name
        systole, diastole = map(int, blood_pressure.split('/'))
        vitals_data['systole'].append(systole)
        vitals_data['diastole'].append(diastole)

    return JsonResponse({'diagnosis': diagnosis_data, 'vitals': vitals_data})
