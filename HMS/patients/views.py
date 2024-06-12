from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
# Create your views here.


@login_required
def dashboard_view(request):
    doctors = CustomUser.objects.filter(is_staff=True,is_superuser=False)
    context = {
        'doctors':doctors,
    }
    return render(request,'patients/dashboard.html',context)

@login_required
@staff_member_required
def patient_list(request):
    patients = CustomUser.objects.filter(is_staff=False)
    
    context = {
        'patients':patients,
    }
    return render(request, 'patients/patient_list.html',context )




@login_required
def patient_details(request, profile_id):
    patient = get_object_or_404(CustomUser, profile_id=profile_id)
    return render(request, 'patients/patient.html', {'patient': patient})