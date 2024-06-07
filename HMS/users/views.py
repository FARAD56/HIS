from django.shortcuts import render, redirect,get_object_or_404
from .forms import CustomSignUpForm,CustomLoginForm,UserUpdateForm,ProfileModelForm,BookPatientForm
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import CustomUser,ProfileModel,BookPatient
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
    patients = CustomUser.objects.filter(is_staff=False)
    
    context = {
        'patients':patients,
    }
    return render(request, 'patient_list.html',context )

@login_required
@staff_member_required
def book_patient(request):
    if request.method == 'POST':
        book_form = BookPatientForm(request.POST)
        if book_form.is_valid():
            book_form.save()
            return redirect('patient_list')
    else:
        book_form = BookPatientForm()
    
    context = {
        'book_form':book_form
    }
    return render(request,'book_patient.html',context)


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
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    context = {
        'patient': patient
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

@login_required
def medication(request,profile_id):
    return render(request,'medication.html')
