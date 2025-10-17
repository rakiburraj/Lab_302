from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Feedback
from doctors.models import doctor, Appointment
from django.contrib.auth.decorators import login_required

@login_required
def give_feedback(request, doctor_id):
    doctor_obj = get_object_or_404(doctor, id=doctor_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '')

        # Find the last seen appointment for this patient
        appointment = Appointment.objects.filter(doctor=doctor_obj, patient__user=request.user, seen=True).last()

        if appointment and not Feedback.objects.filter(appointment=appointment).exists():
            Feedback.objects.create(
                doctor=doctor_obj,
                patient=request.user,
                appointment=appointment,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Feedback submitted successfully!")
        else:
            messages.error(request, "You have already given feedback for this appointment or appointment not found.")

    return redirect('patient_dashboard')
