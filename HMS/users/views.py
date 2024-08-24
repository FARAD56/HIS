from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import CustomUser,ProfileModel
from django.contrib.auth.decorators import login_required
from appointments.forms import AvailabilityForm
from django.utils import timezone
from appointments.models import BookPatient
from patients.models import Todo


def register(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSignUpForm()
    
    context = {
        'form': form,
    }

    return render(request, "users/register.html", context)


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request,email=email,password=password)
            login(request, user)
            if user.is_staff:
                return redirect('doctor_dashboard',profile_id=user.profile_id)
            else:
                return redirect('dashboard',profile_id = user.profile_id)
        else:
            messages.add_messages(request,messages.Error,'email or password is incorrect')
    else:
        form = CustomLoginForm()

    
    context = {
        'form':form,
    }

    return render(request,'users/login.html',context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def user_profile(request,profile_id):
    user = get_object_or_404(CustomUser, profile_id=profile_id)
    
    # Ensure the user has a ProfileModel
    profile, created = ProfileModel.objects.get_or_create(user=user)
    
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=user)
        p_form = ProfileModelForm(request.POST,request.FILES or None,instance=profile)
        if not request.user.is_staff:
            # Ensure staff-only field is not validated for non-staff
            p_form.fields.pop('speciality', None)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user_profile',profile_id=profile_id)
        else:
            # Print form errors to debug
            print(u_form.errors)
            print(p_form.errors)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileModelForm(instance=profile)
        # availability_form = AvailabilityForm()
        if not request.user.is_staff:
            p_form.fields.pop('speciality')
    
    # Ensure availability_form is included in the context
    availability_form = AvailabilityForm()
    context = {
        'u_form': u_form,
        'p_form':p_form,
        'patient': user,
        'availability_form':availability_form,
    }

    return render(request, 'users/user_profile.html', context)


@login_required
def chats(request,profile_id):
    
    return render(request,'chats/chats.html')



@login_required
def doctor_dashboard(request,profile_id):
    doctor = get_object_or_404(CustomUser, profile_id=profile_id)
    # Get the current day and time
    now = timezone.now()
    current_day = now.strftime('%A').upper()  # Converts to full uppercase weekday name
    current_time = now.time()

    # Filter appointments based on availability date and time
    appointments = doctor.doctor_appointments.filter(
        availability__day__gte=current_day,
        availability__time__gte=current_time
    ).order_by('availability__day', 'availability__time')

    # Get all patients diagnosed by the doctor, ensuring no duplicates
    patients_diagnosed = CustomUser.objects.filter(patient_diagnosis__doctor=doctor).distinct()

    user_todos = Todo.objects.filter(user=request.user).order_by('deadline')


    context = {
        'doctor':doctor,
        'appointments':appointments,
        'patients_diagnosed':patients_diagnosed,
        'user_todos':user_todos,

    }
    return render(request,'users/doctor_dashboard.html',context)
