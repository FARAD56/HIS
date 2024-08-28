from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import CustomUser,ProfileModel
from django.contrib.auth.decorators import login_required
from appointments.forms import AvailabilityForm
from appointments.models import BookPatient
from patients.models import Todo
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils.timezone import now
from medicals.models import Diagnosis
from django.db.models import Count


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
@staff_member_required
def doctor_dashboard(request,profile_id):
    doctor = get_object_or_404(CustomUser, profile_id=profile_id)
    
    
    # Get all appointments for the doctor
    future_appointments = doctor.doctor_appointments.all().order_by('-availability__day', 'availability__time')

    # Get all patients diagnosed by the doctor, ensuring no duplicates
    patients_diagnosed = CustomUser.objects.filter(patient_diagnosis__doctor=doctor).distinct()

    user_todos = Todo.objects.filter(user=request.user).order_by('deadline')


    context = {
        'doctor':doctor,
        'future_appointments':future_appointments,
        'patients_diagnosed':patients_diagnosed,
        'user_todos':user_todos,

    }
    return render(request,'users/doctor_dashboard.html',context)

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

   # Count men and women
    men_count = CustomUser.objects.filter(sex='Male').count()
    women_count = CustomUser.objects.filter(sex='Female').count()

    # Calculate current date for age calculation
    today = datetime.today()

    # Count children (e.g., age < 18)
    children_count = CustomUser.objects.filter(
        dob__isnull=False,
        dob__lte=today.replace(year=today.year - 18)
    ).count()

    # Prepare the gender and age group data in the same format
    gender_age_labels = ['Men', 'Women', 'Children']
    gender_age_data = [men_count, women_count, children_count]

    gender_age_chart_data = {
        'labels': gender_age_labels,
        'data': gender_age_data
    }

    # Return all the data as a JSON response
    return JsonResponse({
        'diagnosis': diagnosis_data,
        'gender_age': gender_age_chart_data
    })