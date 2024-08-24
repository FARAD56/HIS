from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['task', 'deadline']
        widgets = {
            'task': forms.TextInput(attrs={
                'class': 'my-2 bg-slate-200 p-2 border border-black w-[90%] sm:w-[80%] rounded-lg',
                'placeholder': 'Add Activity'
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'my-2 bg-slate-200 p-2 border border-black w-[90%] sm:w-[80%] rounded-lg',
                'type': 'datetime-local',  # This allows you to select both date and time
            }),
        }
