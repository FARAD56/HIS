from . import views
from django.urls import path


urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/',  views.register, name='register'),
    path('user-profile/<int:profile_id>/',  views.user_profile, name='user_profile'),
    path('doctor/<int:profile_id>/',  views.doctor_dashboard, name='doctor_dashboard'),
    path('chart/',  views.get_chart_data, name='chart_data'),
]
