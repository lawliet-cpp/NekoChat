from django.shortcuts import render
import redis
import json
import re
def index(request):
    return render(request,"index.html")

def room(request,room_name):
    username = request.GET.get("username","Anonymous")
    r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
    messages =r.smembers(room_name)
    results = []  

    for message in messages:
        content,username = message.split("_")
        message = {
            "username":username,
            "content":content
        }
        results.append(message)
   
    return render(request,"room.html",{"username":username,"room_name":room_name,"messages":results})