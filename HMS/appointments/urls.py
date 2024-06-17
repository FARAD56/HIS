
from . import views
from django.urls import path


urlpatterns = [
    
    path('appointment-dashboard/',  views.appointment_dashboard, name='appointment_dashboard'),
    path('session-dashboard/<int:profile_id>/',  views.session_dashboard, name='session_dashboard'),
    path('book-appointment/<int:profile_id>/',  views.book_appointment, name='book_appointment'),
    path('book-patient/',  views.book_patient, name='book_patient'),
]