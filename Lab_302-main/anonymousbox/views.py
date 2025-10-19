from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AnonymousMessageForm

def send_message(request):
    if request.method == 'POST':
        form = AnonymousMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully! ✅")
            return redirect('send_message')
    else:
        form = AnonymousMessageForm()
    return render(request, 'send_message.html', {'form': form})
from django.shortcuts import render
from .models import AnonymousMessage

def view_messages(request):
    # Show all messages that have a reply
    messages_list = AnonymousMessage.objects.filter(is_replied=True).order_by('-created_at')
    return render(request, 'view_messages.html', {'messages_list': messages_list})

