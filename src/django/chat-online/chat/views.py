from django.shortcuts import render
from django.http import HttpResponse
from .models import Message, Room

def home(request):
    return render(request, 'chat/home.html', {
        'rooms': Room.objects.all(),
        'messages': Message.objects.all(),        
    })