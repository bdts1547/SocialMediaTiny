from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib import messages

import pyrebase

from .models import *
from .serializers import *
from .utils import *



# config = {
#     "apiKey": "AIzaSyDhmSxzNJ28xPy1O8tsb28oSElHVqjqRn8",
#     "authDomain": "socialmediatiny.firebaseapp.com",
#     "projectId": "socialmediatiny",
#     "storageBucket": "socialmediatiny.appspot.com",
#     "messagingSenderId": "868327078831",
#     "appId": "1:868327078831:web:c5c0d1693875307bcb4d5a",
#     "measurementId": "G-7VZ5YK1BTY",
#     "storageBucket": "socialmediatiny.appspot.com",
#     "databaseURL": "https://socialmediatiny-default-rtdb.firebaseio.com/",
# }

# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()

# from SocialMediaTiny import settings
# from pathlib import Path
# Create your views here.

# 1 + i2.jpg 

# class TestView(View):
#     def get(self, request):
#         profiles = Profile.objects.all()
#         url = profiles[0].image.url # /media/profile_iamges/i2.jpg
      
#         ss = str(settings.BASE_DIR) + str(Path(url))
 
#         storage.child(url).put(ss) # Store image to Firebase
        
#         link_url = storage.child(url).get_url(None) # Get url from firebase
#         return render(request, 'test.html', {
#             'profiles': profiles,
#             'link': link_url,
#         }) 


class HomeView(View):
    def get(self, request):


        return render(request, 'home.html', {

        })
    

class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/signin/')

class SignInView(View):
    def get(self, request):


        return render(request, 'signin.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user_login = auth.authenticate(username=username, password=password)
        if user_login is not None:
            auth.login(request, user_login)
            return JsonResponse({'redirect': '/'})
        else:
            return JsonResponse({'error': "Username or password wrong"})
    

class RegisterView(APIView):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        is_succeed = True
        errors = check_error_accout(username, email, password, password2)
        if not errors: # Not error
            # if User.objects.filter(username=username).exists():
            #     messages.info(request, "Username Taken")
            #     errors['username'] = "Username Taken"
            #     is_succeed = False
            # if User.objects.filter(email=email).exists():
            #     messages.info(request, "Email Taken")
            #     errors['email'] = "Email Taken"

            #     is_succeed = False
            
            # if is_succeed:
            #     # hashed_pass = make_password(password)
            #     # new_user = User.objects.create(username=username, email=email, password=hashed_pass)
            #     # new_user.save()
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save() 
            

            #     # Login 
            # user_login = auth.authenticate(username=username, password=password)
            # auth.login(request, user_login)



            # breakpoint()
            return JsonResponse({'redirect': True})
            # else: return redirect('/register/')
        else:
            
            return JsonResponse(errors)


            
        
