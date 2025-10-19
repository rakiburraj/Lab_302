from django.contrib import admin

# Register your models here.
from .models import doctor,department,DoctorProfile,Appointment, DoctorAvailability,PatientProfile,Prescription,Test
admin.site.register(doctor)
admin.site.register(department)
admin.site.register(DoctorProfile)
admin.site.register(Appointment)
admin.site.register(DoctorAvailability)
admin.site.register(PatientProfile) 
admin.site.register(Prescription)
admin.site.register(Test)