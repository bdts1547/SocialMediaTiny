from django.contrib.auth.models import User
from .models import *
import uuid

data = {
    'username': 'dang',
    'email': 'dang@da.c',
    'password': '123',
    'password2': '123',
}


def check_error_accout(username, email, password, password2):
    errors = {}
    if User.objects.filter(username=username).exists():
        errors['username'] = "Username Taken"
    if User.objects.filter(email=email).exists():
        errors['email'] = "Email Taken"
    if password != password2:
        errors['password'] = "Password not matching"

    return errors


def save_image_post_to_firebase(storage, image, post):
    id = str(uuid.uuid4())
    dest = f'media/post_images/{id}.jpg'
    storage.child(dest).put(image) # Save to firebase storage
    image_path = storage.child(dest).get_url(None)

    add_img = ImagesOfPost.objects.create(id=id, post=post, image_path=image_path)
    add_img.save()
    
    return True

