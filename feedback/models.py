from django.db import models
from django.contrib.auth.models import User
from doctors.models import doctor, Appointment

class Feedback(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE, related_name='feedback_set')
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.rating}⭐ for {self.doctor.name}"
