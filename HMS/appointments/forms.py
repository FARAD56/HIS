from .models import BookPatient,Availability,Appointment
from django import forms


class BookPatientForm(forms.ModelForm):
    class Meta:
        model = BookPatient
        fields = ['patient_id','temperature','blood_pressure','triage','comments']
        widgets = {
            'patient_id': forms.TextInput(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full',
                'placeholder':'Patient Id'
            }),
            'temperature': forms.TextInput(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full',
                'placeholder': 'Temperature'
            }),
            'blood_pressure': forms.TextInput(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full',
                'placeholder': 'Blood Pressure'
            }),
            'triage': forms.Select(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full',
                'placeholder': 'Comments'
            }),
        }


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['doctor_id','day', 'time','type']
        widgets = {
            'doctor_id': forms.TextInput(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full',
                'placeholder': 'Id',
                'type': 'id'}),
            'day': forms.Select(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full',
                'placeholder': 'day of the week',
                }),
            'time': forms.TimeInput(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full',
                'placeholder': 'Enter Time',
                'type': 'time'}),
            'type': forms.Select(attrs={
                'class': 'bg-slate-200 p-2 border border-blue-300 rounded-lg w-full',
                'rows': 3}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'placeholder':"Add a comment",
                'class':"border border-slate-600 rounded-lg p-2 w-3/5",
                'rows': 3}),
        }