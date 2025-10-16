from django import forms
from .models import doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = doctor
        fields = ['name', 'specialization', 'phone_number', 'email']

class DepartmentForm(forms.Form):
    class Meta:
        model = doctor
        fields = ['name', 'head']   

from django import forms
from .models import PatientProfile

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['profile_picture', 'name', 'gender', 'age', 'blood_group']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }        
from django import forms
from .models import DoctorAvailability, Appointment, PatientProfile

class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['day', 'start_time', 'end_time', 'patient_limit','fee']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'patient_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['name', 'age', 'gender', 'blood_group', 'profile_picture']


from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription_image'] 
from django import forms
from .models import doctor

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = doctor
        fields = ['name', 'specialization', 'phone_number', 'email', 'department', 'photo', 'education', 'experience', 'consultation_fee']        