from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import CustomUser,ProfileModel
from django.contrib.auth.decorators import login_required
from appointments.forms import AvailabilityForm

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

            return redirect('dashboard')
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
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    
    # Ensure the user has a ProfileModel
    profile, created = ProfileModel.objects.get_or_create(user=patient)
    
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=patient)
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
        u_form = UserUpdateForm(instance=patient)
        p_form = ProfileModelForm(instance=profile)
        # availability_form = AvailabilityForm()
        if not request.user.is_staff:
            p_form.fields.pop('speciality')
    
    # Ensure availability_form is included in the context
    availability_form = AvailabilityForm()
    context = {
        'u_form': u_form,
        'p_form':p_form,
        'patient': patient,
        'availability_form':availability_form,
    }

    return render(request, 'users/user_profile.html', context)


@login_required
def chats(request,profile_id):
    
    return render(request,'chats/chats.html')


