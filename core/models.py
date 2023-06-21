# from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

import uuid
from datetime import datetime


User = get_user_model()




# Create your models here.
class Profile(models.Model):
    GENDER_CHOICE = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    about_me = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.CharField(max_length=100000, default='media/profile_images/blank_profile.png')
    gender = models.CharField(max_length=1, default="M", choices=GENDER_CHOICE)

    def __str__(self) -> str:
        return self.user.username
  
    
    


