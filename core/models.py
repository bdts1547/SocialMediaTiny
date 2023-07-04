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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    about_me = models.TextField(blank=True, default="")
    location = models.CharField(max_length=255, default="", blank=True)
    image_path = models.CharField(max_length=100000, default='https://firebasestorage.googleapis.com/v0/b/socialmediatiny.appspot.com/o/media%2Fprofile_images%2Fblank_profile.png?alt=media&token=a7798e1c-3621-486e-b025-1befb1c0caf8')
    university = models.CharField(max_length=255, blank=True, default="")
    gender = models.CharField(max_length=1, default="M", choices=GENDER_CHOICE)

    def __str__(self) -> str:
        return self.user.username
  

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)
    is_enabled_comments = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class ImagesOfPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_path = models.CharField(max_length=100000, default="")



class LikeOfPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')


class CommentOfPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    comment = models.CharField(max_length=10000, null=True, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username + " " + self.comment
    


