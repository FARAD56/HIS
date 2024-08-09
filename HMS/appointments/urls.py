
from . import views
from django.urls import path


urlpatterns = [
    
    path('appointment-dashboard/',  views.appointment_dashboard, name='appointment_dashboard'),
    path('session-dashboard/<int:profile_id>/',  views.session_dashboard, name='session_dashboard'),
    path('google-calendar-init/', views.google_calendar_init, name='google_calendar_init'),
    path('oauth2callback/', views.google_calendar_callback, name='google_calendar_callback'),

    path('book-appointment/<int:profile_id>/',  views.book_appointment, name='book_appointment'),
    path('book-patient/',  views.book_patient, name='book_patient'),
    path('availability/<int:profile_id>/',  views.doctor_availability, name='availability'),
]