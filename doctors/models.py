from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
  

class doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # link to Django user
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    department = models.ForeignKey('department', on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.name} - {self.specialization}'
    def average_rating(self):
        avg = self.feedback_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0




    
class department(models.Model):
    name = models.CharField(max_length=100)
    head = models.CharField(max_length=100)

    def __str__(self):
        return self.name    
    
from django.contrib.auth.models import User
from django.db import models

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    # other doctor fields    

# models.py





from django.db import models
from django.contrib.auth.models import User

# models.py
DAYS_OF_WEEK = [
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
]

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)  # allow empty
    end_time = models.TimeField(default='00:00')    # allow empty
    patient_limit = models.PositiveIntegerField(default=20)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=500)


    def __str__(self):
        return f"{self.doctor.name} - {self.get_day_display()} ({self.start_time}-{self.end_time})"

from django.db import models
from django.contrib.auth.models import User

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    name = models.CharField(max_length=100)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    age = models.PositiveIntegerField()
    blood_group_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    blood_group = models.CharField(max_length=3, choices=blood_group_choices)

    def __str__(self):
        return self.name
class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    result_file = models.FileField(upload_to='test_reports/', blank=True, null=True)
    


    class Meta:
        unique_together = ('doctor', 'date', 'time')  # Prevent double booking

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.date} at {self.time}"    
class Test(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    result_file = models.FileField(upload_to='test_reports/', blank=True, null=True)

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    prescription_image = models.ImageField(upload_to='prescriptions/')




