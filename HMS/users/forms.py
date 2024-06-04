from django import forms
from .models import CustomUser,ProfileModel,PatientVital
from django.contrib.auth.hashers import make_password




class CustomSignUpForm(forms.Form):
    SEX_CHOICES = (('Male', 'Male'), ('Female', 'Female'))

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={
        'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'First Name',
    }))
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={
        'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'Last Name',
    })
    )
    contact = forms.CharField(
        label='Contact',
        widget=forms.TextInput(attrs={
        'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'Phone Number 10 digits',
    })
    )
    dob = forms.DateField(
        label=' DOB',
        widget=forms.DateInput(attrs={
        'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'Date of Birth',
    }),
    
    input_formats=['%d/%m/%Y', '%d-%m-%Y'],
    )
    sex = forms.ChoiceField(
        label='Sex',
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={
            'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
            'placeholder': 'Select One'
        }),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
        'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'Email',
    }))
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
        'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'Enter Password',
    })
    )
    confirm_password  = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
        'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'Confirm Password',
    })
    )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        user = CustomUser(
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            email=cleaned_data['email'],
            username=cleaned_data['email'],  
            contact=cleaned_data['contact'],  
            dob=cleaned_data['dob'],
            sex=cleaned_data['sex'],
            password=make_password(cleaned_data['password']),  # Hash the password
        )
        user.save()
        return user
    


class CustomLoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
         'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'EMAIL',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
        'placeholder': 'PASSWORD',
    }))
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','contact','email']
    
    # def __init__(self, *args, **kwargs) -> None:
    #     super(UserUpdateForm,self).__init__(*args, **kwargs)
        
    #     for fieldname in ['username','email']:
    #         self.fields[fieldname].help_text = None

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['profile_picture','religion','place_of_birth','marital_status',
                  'nationality','occupation','region','address','kin_name','kin_address',
                  'relationship','kin_contact','kin_email']
        
class PatientVitalsForm(forms.ModelForm):
    class Meta:
        model = PatientVital
        fields = ['user','temperature','blood_pressure','triage','comments']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
                # 'placeholder':'patient_id'
            }),
            'temperature': forms.TextInput(attrs={
                'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
                'placeholder': 'Temperature'
            }),
            'blood_pressure': forms.TextInput(attrs={
                'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
                'placeholder': 'Blood Pressure'
            }),
            'triage': forms.Select(attrs={
                'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'bg-slate-200 p-2 border border-black rounded-lg w-full',
                'placeholder': 'Comments'
            }),
        }



