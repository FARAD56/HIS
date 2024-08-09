from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import BookPatientForm,AppointmentForm
from users.models import CustomUser
from django.db.models import Q
from .models import Availability,Appointment
# Create your views here.
from .forms import AvailabilityForm
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import datetime
import pytz
from django.shortcuts import redirect
from django.conf import settings
import os

def google_calendar_init(request):
    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    flow = InstalledAppFlow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=settings.GOOGLE_API_SCOPES
    )
    flow.redirect_uri = request.build_absolute_uri('/sessions/oauth2callback/')
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return redirect(authorization_url)

def google_calendar_callback(request):
    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    state = request.session['state']
    flow = InstalledAppFlow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=settings.GOOGLE_API_SCOPES,
        state=state
    )
    flow.redirect_uri = request.build_absolute_uri('/sessions/oauth2callback/')
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect('session_dashboard',request.user.profile_id)



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

#to book an appoitnment with a doctor
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
                appointment.patient = request.user
                appointment.doctor = doctor
                appointment.save()

                # Create Google Calendar event
                if 'credentials' not in request.session:
                    return redirect('google_calendar_init')


                os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Disable HTTPS requirement for local development
                credentials = Credentials(**request.session['credentials'])
                service = build('calendar', 'v3', credentials=credentials)

                # Get the current date
                today = datetime.date.today()
                # Find the next occurrence of the availability day
                days_ahead = (Availability.Day[availability.day.upper()].value - today.weekday()) % 7
                appointment_date = today + datetime.timedelta(days=days_ahead)

                # Set the start and end time for the event
                start_time = datetime.datetime.combine(appointment_date, availability.time)
                end_time = start_time + datetime.timedelta(hours=2)
                
                # Ensure times are in UTC
                start_time_utc = pytz.utc.localize(start_time)
                end_time_utc = pytz.utc.localize(end_time)
                event = {
                    'summary': f'Appointment with Dr. {doctor.get_full_name()}',
                    'description': 'Appointment booked through the health management system.',
                    'start': {
                        'dateTime': start_time_utc.isoformat(),
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': end_time_utc.isoformat(),
                        'timeZone': 'UTC',
                    },
                    'attendees': [
                        {'email': request.user.email},
                        {'email': doctor.email},
                    ],
                    'conferenceData': {
                        'createRequest': {
                            'requestId': 'sample123',
                            'conferenceSolutionKey': {
                                'type': 'hangoutsMeet',
                            },
                        },
                    },
                }

                event = service.events().insert(
                    calendarId='primary',
                    body=event,
                    conferenceDataVersion=1,
                ).execute()

                print(f"Created Google Meet link: {event['hangoutLink']}")
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
    if user.is_staff:
        appointments = Appointment.objects.filter(doctor=user)
    else:
        appointments = Appointment.objects.filter(patient=user)

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


@login_required
def doctor_availability(request, profile_id):
    if request.method == 'POST':
        availability_form = AvailabilityForm(request.POST)

        if availability_form.is_valid():
            availability_form.save()
            return redirect('user_profile', profile_id=profile_id)
        else:
            print(availability_form.errors)
    else:
        availability_form = AvailabilityForm()

    # Pass the form to the template
    context = {
        'availability_form': availability_form,
        # Include other context variables needed for rendering the user_profile template
    }

    return render(request, 'users/user_profile.html', context)