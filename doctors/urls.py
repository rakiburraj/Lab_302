from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
   path('departments/', views.department_list, name='department_list'),
   path('doctors/', views.doctor_list, name='doctor_list'),
   path('patient_register/', views.patient_register, name='patient_register'),
   path('patient_login/', views.patient_login, name='patient_login'),
   path('doctor_login/', views.doctor_login, name='doctor_login'),
   path('department/<int:dept_id>/', views.department_detail, name='department_detail'),
   path('doctor/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
   path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
   path('department/<int:department_id>/doctors/', views.department_doctors, name='department_doctors'),
   path('doctor/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'),
   path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
   path('doctor/set-availability/', views.set_availability, name='set_availability'),
   path('appointment/<int:appointment_id>/add-prescription/', views.add_prescription, name='add_prescription'),
   path('doctor/view-patient/<int:patient_id>/', views.view_patient, name='view_patient'),
   path('profile/', views.profile_detail, name='profile_detail'),
   path('create-profile/', views.create_patient_profile, name='create_patient_profile'),
   path('edit-profile/', views.edit_patient_profile, name='edit_patient_profile'),
   path('book-appointment/', views.book_appointment, name='book_appointment'),  # all doctors
   path('doctor/<int:doctor_id>/book/', views.book_appointment, name='book_appointment_for_doctor'),
   path('appointment/<int:appointment_id>/pay/', views.pay_appointment, name='pay_appointment'),
   path('doctor/mark-seen/<int:appointment_id>/', views.mark_seen, name='mark_seen'),
   path('submit_feedback/<int:appointment_id>/', views.submit_feedback, name='submit_feedback'),
   path('doctor/edit-profile/', views.edit_doctor_profile, name='edit_doctor_profile'),
   
]
