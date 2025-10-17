from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Feedback
from doctors.models import doctor, Appointment
from django.contrib.auth.decorators import login_required



