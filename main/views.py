from django.shortcuts import render
from .models import Room
import json
import re
def index(request):
    return render(request,"index.html")

def room(request,room_name):
    username = request.GET.get("username","Anonymous")
    room,created = Room.objects.get_or_create(name=room_name)
    messages = room.messages.all()
   
    return render(request,"room.html",{"username":username,"room_name":room_name,"messages":messages})