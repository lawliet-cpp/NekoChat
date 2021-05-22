from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=155,unique=True)
    
class Message(models.Model):
    content = models.TextField()
    username = models.CharField(max_length=31)
    room = models.ForeignKey(Room,related_name="messages",on_delete=models.CASCADE)
