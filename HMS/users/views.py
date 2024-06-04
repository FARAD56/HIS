from django.shortcuts import render, redirect,get_object_or_404
from .forms import CustomSignUpForm,CustomLoginForm,UserUpdateForm,ProfileModelForm,PatientVitalsForm
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import CustomUser,ProfileModel,PatientVital
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



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

    return render(request, "register.html", context)


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request,email=email,password=password)
            login(request, user)

            return redirect('dashboard')
        else:
            messages.add_messages(request,messages.Error,'email or password is incorrect')
    else:
        form = CustomLoginForm()

    
    context = {
        'form':form,
    }

    return render(request,'login.html',context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    
    return render(request,'dashboard.html')

@login_required
@staff_member_required
def patient_list(request):
    # patients = CustomUser.objects.filter(is_staff=False)
    critical_patients = PatientVital.objects.filter(triage=PatientVital.Triage.CRITICAL)
    severe_patients = PatientVital.objects.filter(triage=PatientVital.Triage.SEVERE)
    normal_patients = PatientVital.objects.filter(triage=PatientVital.Triage.NORMAL)
    all_patients = PatientVital.objects.all()
    
    context = {
        'critical_patients': critical_patients,
        'severe_patients': severe_patients,
        'normal_patients': normal_patients,
        'all_patients': all_patients,
        # 'patients':patients,
    }
    return render(request, 'patient_list.html',context )

@login_required
@staff_member_required
def patient_vitals(request):
    if request.method == 'POST':
        v_form = PatientVitalsForm(request.POST)
        if v_form.is_valid():
            v_form.save()
            return redirect('patient_list')
    else:
        v_form = PatientVitalsForm()
    
    context = {
        'v_form':v_form
    }
    return render(request,'patient_vitals.html',context)


@login_required
def patient_details(request, profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    return render(request, 'patient.html', {'patient': patient})

@login_required
def patient_profile(request,profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    
    # Ensure the user has a ProfileModel
    profile, created = ProfileModel.objects.get_or_create(user=patient)
    
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=patient)
        p_form = ProfileModelForm(request.POST,request.FILES or None,instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('patient_profile',profile_id=profile_id)
    else:
        u_form = UserUpdateForm(instance=patient)
        p_form = ProfileModelForm(instance=profile)
    
    context = {
        'u_form': u_form,
        'p_form':p_form,
        'patient': patient,
        
    }

    return render(request, 'patient_profile.html', context)

@login_required
def patient_attendance(request,profile_id):
    context = {
    }

    return render(request, 'patient_attendance_details.html', context)

@login_required
@staff_member_required
def medical_record(request,profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    context = {
        'patient': patient
    }

    return render(request,'medical_records.html',context)

@login_required
def session_dashboard(request,profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    # 
    return render(request,'session_dashboard.html')

@login_required
def chats(request,profile_id):
    
    return render(request,'chats.html')

@login_required
def book_appointment(request,profile_id):
    return render(request,'book_appointment.html')
