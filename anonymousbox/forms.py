from django import forms
from .models import AnonymousMessage

class AnonymousMessageForm(forms.ModelForm):
    class Meta:
        model = AnonymousMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your message...'}),
        }
