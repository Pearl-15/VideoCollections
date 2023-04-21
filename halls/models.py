from django.db import models
from django.contrib.auth.models import User

# one Hall can have many videos
class Hall(models.Model):
    title = models.CharField(max_length=255)
    '''
    purpose : to know which hall is created by which user
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #one user can have many Halls

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)  #one Hall can have many Videos
