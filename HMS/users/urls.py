from . import views
from django.urls import path


urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/',  views.register, name='register'),

    path('dashboard/',  views.dashboard_view, name='dashboard'),
    path('patient-list/',  views.patient_list, name='patient_list'),
    path('book-patient/',  views.book_patient, name='book_patient'),

    path('patient/<int:profile_id>/',  views.patient_details, name='patient_details'),
    path('patient-profile/<int:profile_id>/',  views.patient_profile, name='patient_profile'),
    path('patient-attendance/<int:profile_id>/',  views.patient_attendance, name='patient_attendance'),
    path('medical-record/<int:profile_id>/',  views.medical_record, name='medical_record'),
    path('medication/<int:profile_id>/',  views.medication, name='medication'),

    path('session-dashboard/<int:profile_id>/',  views.session_dashboard, name='session_dashboard'),
    path('chats/<int:profile_id>/',  views.chats, name='chats'),
    path('book-appointment/<int:profile_id>/',  views.book_appointment, name='book_appointment'),

]
