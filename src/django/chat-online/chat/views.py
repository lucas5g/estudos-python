import json
from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from .models import Message, Room
from django.views.generic.detail import DetailView 

def home(request):
    return render(request, 'chat/home.html', {
        'rooms': Room.objects.all(),
    })
    
    
class RoomDetailView(DetailView):
    model = Room 
    template_name = 'chat/list-messages.html'    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)
    
def send_message(request, pk):
    data = json.loads(request.body)
    print(data)
    new_message = Message.objects.create(user= request.user, text=data['message'])
        
    return render(request, "chat/home.html", {
        "m": new_message
    })