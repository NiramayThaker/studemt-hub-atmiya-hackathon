from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    # For just specifing name of the Topic and giving its reference to Room topic field
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    """Model for specific Room(entity)"""

    # For details of host 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Somebody have to host the room and then set the topic of it

    # Sets the topic of the room by inheriting it from Topic Class(model) and if topic is deleted room is just set NULL not deleted
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    # For Name 
    name = models.CharField(max_length=200)  

    # To save the description null=True means that form could be submitted blank
    description = models.TextField(null=True, blank=True)  
    
    # It specifies that the specific "USER" will have many to many relationship
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    # Blank true as it will submit the form without checking

    # To keep the last track of updated value "auto_now=True" return currrent time
    updated = models.DateTimeField(auto_now=True)

    # To save the date/time when table was created "auto_now_add=True" just keeps first value of the change occured
    created = models.DateTimeField(auto_now_add=True)  # It will never change (used for initial time stamp)

    def __str__(self):
        """Used for string representation of data being showed outside"""
        return self.name
    
    class Meta:
        # For printing newest item first in page
        ordering = ['-updated', '-created']


class Message(models.Model):
    """Model for showing message that user has entered"""

    # user wull have One to many relationships as one user can have multiple message but message can only have one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Joining table using foreign key(when room is deleted all data related to it will be cascaded[deleted]))
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    # Body field for actual message 
    body = models.TextField()

    # To keep the last track of updated value "auto_now=True" return currrent time
    updated = models.DateTimeField(auto_now=True)

    # To save the date/time when table was created "auto_now_add=True" just keeps first value of the change occured
    created = models.DateTimeField(auto_now_add=True)  # It will never change (used for initial time stamp)

    class Meta:
        # For printing newest item first in page
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        # Will display first 50 words of msg(body) as title
        return self.body[0:50]


class LikeModel(models.Model):
    like_count = models.IntegerField(default=0)
    room_liked = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_liked = models.ForeignKey(User, on_delete=models.CASCADE)
