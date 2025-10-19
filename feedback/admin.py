from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'appointment', 'rating', 'created_at')
    list_filter = ('doctor', 'rating')
    search_fields = ('doctor__name', 'patient__username', 'comment')
