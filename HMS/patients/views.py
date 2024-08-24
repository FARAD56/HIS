from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
from users.models import ProfileModel
from appointments.models import BookPatient
from django.db.models import Q
from medicals.models import Prescription
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm

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
    user_todos = Todo.objects.filter(user=request.user).order_by('deadline')

    context = {
        'diagnosed_doctors': diagnosed_doctors,  # Use the filtered doctors
        'medications': medications,
        'patient': patient,
        'appointments': appointments,
        'user_todos':user_todos,
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


class TodoListView(ListView):
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('deadline')

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