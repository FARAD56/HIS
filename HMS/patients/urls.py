from . import views
from django.urls import path

urlpatterns = [
    path('dashboard/<int:profile_id>',  views.dashboard_view, name='dashboard'),
    path('patient-list/',  views.patient_list, name='patient_list'),
    path('patient/<int:profile_id>/',  views.patient_details, name='patient_details'),
    path('add-activity/',  views.TodoCreateView.as_view(), name='add_activity'),
    path('edit-activity/<int:id>/',  views.TodoUpdateView.as_view(), name='edit_activity'),
    path('delete-activity/<int:id>/',  views.TodoDeleteView.as_view(), name='delete_activity'),
    path('complete_activity/<int:id>/',  views.TodoCompleteView.as_view(), name='complete_activity'),
    path('chart/',  views.get_chart_data, name='chart_data'),
]