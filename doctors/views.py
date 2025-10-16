from datetime import timezone
from django.shortcuts import render,redirect
from .forms import DoctorAvailabilityForm, DoctorForm, DoctorProfileForm, PrescriptionForm
from .models import DoctorAvailability, department,doctor
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def department_list(request):
    departments = department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def doctor_list(request):
    doctors = doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})
def patient_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            # Optionally create PatientProfile here
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('patient_login')
    return render(request, 'patient_register.html')
from django.contrib.auth import authenticate, login

def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'patient_login.html')
def doctor_login(request):
    # Your login logic here
    return render(request, 'doctor_login.html')
def department_detail(request, dept_id):
    dept = department.objects.get(id=dept_id)
    doctors = doctor.objects.filter(department=dept)
    return render(request, 'department_detail.html', {'department': dept, 'doctors': doctors})
def doctor_profile(request, doctor_id):
    doc = doctor.objects.get(id=doctor_id)
    return render(request, 'doctor_profile.html', {'doc': doc})
# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from doctors.models import Appointment, Prescription
from .models import PatientProfile, department

@login_required
def patient_dashboard(request):
    user = request.user  # logged-in user

    # Departments
    departments = department.objects.all()

    # Patient profile
    try:
        profile = PatientProfile.objects.get(user=user)
        profile_exists = True
        patient_name = profile.name
    except PatientProfile.DoesNotExist:
        profile_exists = False
        patient_name = user.username  # fallback

    # Appointments
    if profile_exists:
        appointments = Appointment.objects.filter(patient=profile).order_by('-date', 'time')
        # You no longer need to attach prescriptions manually,
        # template will handle Prescription.objects.filter(appointment=app)
    else:
        appointments = []

    context = {
        'departments': departments,
        'profile_exists': profile_exists,
        'patient_name': patient_name,
        'appointments': appointments,
    }

    return render(request, 'patient_dashboard.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import department, doctor, Appointment

def department_doctors(request, department_id):
    dept = get_object_or_404(department, id=department_id)
    doctors = doctor.objects.filter(department=dept)

    return render(request, 'department_doctors.html', {
        'department': dept,
        'doctors': doctors
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime as dt
from .models import doctor, DoctorAvailability, Appointment
from .forms import PatientProfileForm

@login_required
def book_appointment(request, doctor_id=None):
    patient = request.user.patientprofile
    doctors = doctor.objects.all()  # list of doctors
    available_dates_times = {}

    # Generate slots for next 30 days
    for doc in doctors:
        availabilities = DoctorAvailability.objects.filter(doctor=doc)
        dates_times = {}
        for i in range(30):
            date_obj = timezone.localtime().date() + timedelta(days=i)
            day_code = date_obj.strftime('%a').lower()  # mon, tue, etc.

            if availabilities.filter(day=day_code).exists():
                slot_obj = availabilities.get(day=day_code)
                start = slot_obj.start_time
                end = slot_obj.end_time
                slots = []
                current_time = dt.combine(date_obj, start)
                end_datetime = dt.combine(date_obj, end)

                while current_time < end_datetime:
                    if not Appointment.objects.filter(
                        doctor=doc,
                        date=date_obj,
                        time=current_time.time()
                    ).exists():
                        slots.append(current_time.time().strftime('%H:%M'))
                    current_time += timedelta(minutes=30)

                if slots:
                    dates_times[date_obj.strftime('%Y-%m-%d')] = slots

        available_dates_times[doc.id] = dates_times

    # Handle appointment booking form
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        notes = request.POST.get('notes', '')
        doc = doctor.objects.get(id=doctor_id)
        date_obj = dt.strptime(date_str, '%Y-%m-%d').date()
        time_obj = dt.strptime(time_str, '%H:%M').time()

        # Check if slot is already booked
        if Appointment.objects.filter(doctor=doc, date=date_obj, time=time_obj).exists():
            error = "Selected time is already booked."
            return render(request, 'book_appointment.html', {
                'doctors': doctors,
                'available_dates_times': available_dates_times,
                'error': error
            })

        # Create appointment
        Appointment.objects.create(
            patient=patient,
            doctor=doc,
            date=date_obj,
            time=time_obj,
            notes=notes,
            is_paid=False
        )
        return redirect('pay_appointment', appointment_id=Appointment.objects.latest('id').id)

    return render(request, 'book_appointment.html', {
        'doctors': doctors,
        'available_dates_times': available_dates_times,
        'selected_doctor_id': doctor_id
    })



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from .models import doctor, Appointment, DoctorAvailability

# Doctor Login
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is linked to a doctor
            if hasattr(user, 'doctor'):
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                return render(request, 'doctor_login.html', {'error': 'This user is not a doctor.'})
        else:
            return render(request, 'doctor_login.html', {'error': 'Invalid username or password.'})
    return render(request, 'doctor_login.html')

# Doctor Dashboard

@login_required
def doctor_availability(request):
    doctor = request.user.doctor  # assuming a OneToOne field from User
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = doctor
            availability.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorAvailabilityForm()
    return render(request, 'doctor_availability.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import doctor, DoctorAvailability

@login_required
def set_availability(request):
    doc_instance = request.user.doctor

    if request.method == 'POST':
        days = request.POST.getlist('days')  # selected weekdays
        max_patients = int(request.POST.get('max_patients', 10))
        fee = int(request.POST.get('fee', 500))  # fee per day

        # Remove old availability
        DoctorAvailability.objects.filter(doctor=doc_instance).delete()

        for day in days:
            DoctorAvailability.objects.create(
                doctor=doc_instance,
                day_of_week=int(day),
                max_patients=max_patients,
                fee=fee
            )

        return redirect('doctor_dashboard')

    return render(request, 'set_availability.html', {
        'days_of_week': DoctorAvailability.DAYS_OF_WEEK
    })

# Upload Prescription
@login_required
def upload_prescription(request, appointment_id):
    doctor_obj = get_object_or_404(doctor, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor_obj)
    if request.method == 'POST' and 'prescription' in request.FILES:
        appointment.prescription = request.FILES['prescription']
        appointment.save()
    return redirect('doctor_dashboard')

# View Patient Profile
from django.shortcuts import get_object_or_404

def view_patient(request, patient_id):
    # Get the PatientProfile instance
    patient = get_object_or_404(PatientProfile, id=patient_id)

    # Now you can query appointments
    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'view_patient.html', {
        'patient': patient,
        'appointments': appointments,
    })
import datetime

def is_doctor_available(doctor_obj, date):
    weekday = date.weekday()  # 0 = Monday, 6 = Sunday
    availability = DoctorAvailability.objects.filter(doctor=doctor_obj, day_of_week=weekday).first()
    if availability:
        booked_count = Appointment.objects.filter(doctor=doctor_obj, date=date).count()
        return booked_count < availability.max_patients
    return False
@login_required
def pay_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        appointment.is_paid = True
        appointment.save()
        return redirect('patient_dashboard')
    return render(request, 'pay_appointment.html', {'appointment': appointment})

# doctors/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PatientProfile
from .forms import PatientProfileForm
from django.contrib import messages

@login_required
def create_patient_profile(request):
    # Check if the user already has a profile
    if PatientProfile.objects.filter(user=request.user).exists():
        messages.info(request, "You already have a profile.")
        return redirect('profile_detail')  # redirect to view profile

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile created successfully!")
            return redirect('profile_detail')
    else:
        form = PatientProfileForm()

    return render(request, 'create_patient_profile.html', {'form': form})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PatientProfile  # since model is in the same app

@login_required
def profile_detail(request):
    """
    Show the logged-in patient's profile.
    """
    try:
        profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        profile = None

    return render(request, 'profile_detail.html', {'profile': profile})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PatientProfile
from .forms import PatientProfileForm
from django.contrib import messages

@login_required
def edit_patient_profile(request):
    profile = get_object_or_404(PatientProfile, user=request.user)

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_detail')
    else:
        form = PatientProfileForm(instance=profile)

    return render(request, 'edit_patient_profile.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time
from .models import doctor, DoctorAvailability, Appointment, Prescription
from .forms import DoctorAvailabilityForm, PrescriptionForm

from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorAvailability, Appointment

DAYS_OF_WEEK = [
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
]

@login_required
def doctor_dashboard(request):
    doc = request.user.doctor
    today = datetime.today().date()

    # Fetch doctor's upcoming appointments
    appointments = Appointment.objects.filter(
        doctor=doc,
        date__gte=today
    ).order_by('date', 'time')

    # Fetch doctor's availability
    doctor_availability = DoctorAvailability.objects.filter(doctor=doc).order_by('day')

    # For pre-checking which days are selected in the form
    selected_days = [avail.day for avail in doctor_availability]

    if request.method == 'POST':
        # Handle availability form submission
        days = request.POST.getlist('days')  # list of selected days
        patient_limit = int(request.POST.get('patient_limit', 10))
        fee = float(request.POST.get('fee', 500))
        start_time = request.POST.get('start_time', '09:00')
        end_time = request.POST.get('end_time', '17:00')

        start_time_obj = datetime.strptime(start_time, '%H:%M').time()
        end_time_obj = datetime.strptime(end_time, '%H:%M').time()

        # Remove availability for unselected days
        DoctorAvailability.objects.filter(doctor=doc).exclude(day__in=days).delete()

        # Update existing availability or create new for selected days
        for day in days:
            DoctorAvailability.objects.update_or_create(
                doctor=doc,
                day=day,
                defaults={
                    'patient_limit': patient_limit,
                    'fee': fee,
                    'start_time': start_time_obj,
                    'end_time': end_time_obj
                }
            )

        return redirect('doctor_dashboard')

    context = {
        'doc': doc,
        'appointments': appointments,
        'doctor_availability': DoctorAvailability.objects.filter(doctor=doc).order_by('day'),  # refresh after POST
        'days_of_week': DAYS_OF_WEEK,
        'selected_days': [avail.day for avail in DoctorAvailability.objects.filter(doctor=doc)],  # refresh after POST
        'default_patient_limit': 10,
        'default_fee': 500,
        'default_start_time': '09:00',
        'default_end_time': '17:00',
    }
    return render(request, 'doctor_dashboard.html', context)



@login_required
def add_prescription(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            presc = form.save(commit=False)
            presc.appointment = appointment
            presc.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'add_prescription.html', {'form': form, 'appointment': appointment})
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def mark_seen(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
    appointment.seen = True
    appointment.save()
    return redirect('doctor_dashboard')
# views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from doctors.models import Appointment
from feedback.models import Feedback
from .models import PatientProfile
from django.contrib.auth.decorators import login_required

@login_required
def submit_feedback(request, appointment_id):
    patient_profile = get_object_or_404(PatientProfile, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient_profile)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '')
        
        feedback, created = Feedback.objects.update_or_create(
            appointment=appointment,
            defaults={
                'rating': rating,
                'comment': comment,
                'doctor': appointment.doctor,
                'patient': request.user  # <-- use User instance
            }
        )
        
        messages.success(request, "Your feedback has been submitted successfully!")
    else:
        messages.error(request, "Invalid request.")
    
    return redirect('patient_dashboard')
@login_required
def edit_doctor_profile(request):
    doc = request.user.doctor

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  # Redirect to dashboard after saving
    else:
        form = DoctorProfileForm(instance=doc)

    return render(request, 'edit_doctor_profile.html', {'form': form})
