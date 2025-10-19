from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='send_message'),
    path('view-messages/', views.view_messages, name='view_messages'),
]
