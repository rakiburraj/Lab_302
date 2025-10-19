from django.urls import path
from . import views

urlpatterns = [
    path('give/<int:doctor_id>/', views.give_feedback, name='give_feedback'),
]