from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView


import pyrebase

from .models import *
from .serializers import *
from .utils import *



config = {
    "apiKey": "AIzaSyDhmSxzNJ28xPy1O8tsb28oSElHVqjqRn8",
    "authDomain": "socialmediatiny.firebaseapp.com",
    "projectId": "socialmediatiny",
    "storageBucket": "socialmediatiny.appspot.com",
    "messagingSenderId": "868327078831",
    "appId": "1:868327078831:web:c5c0d1693875307bcb4d5a",
    "measurementId": "G-7VZ5YK1BTY",
    "storageBucket": "socialmediatiny.appspot.com",
    "databaseURL": "https://socialmediatiny-default-rtdb.firebaseio.com/",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()




class HomeView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        profile_login = Profile.objects.get(user=request.user)
        list_posts = Post.objects.all()
        list_profiles, list_of_list_imagesPost = [], []
        list_of_list_imagesComment, list_of_list_imagesLike = [], []
        for post in list_posts:
            profile = Profile.objects.get(user=post.user)
            list_profiles.append(profile)
            
            list_image_post = ImagesOfPost.objects.filter(post=post)
            list_of_list_imagesPost.append(list_image_post)

            # list_image_like = ImagesOfPost.objects.filter(post=post)
            # list_of_list_imagesLike.append(list_image_like)

            # list_image_comment = ImagesOfPost.objects.filter(post=post)
            # list_of_list_imagesComment.append(list_image_comment)
            
        zip_data = zip(list_posts, list_profiles, list_of_list_imagesPost)
        return render(request, 'home.html', {
            'profile_login': profile_login,
            'list_posts': list_posts,
            'list_profiles': list_profiles,
            'list_of_list_imagesPost': list_of_list_imagesPost,
            'zip_data': zip_data,
        })
    

class Logout(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        auth.logout(request)
        return redirect('/signin/')


class SignInView(View):

    def get(self, request):
        
        return render(request, 'signin.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        redirect_next = request.POST['redirect_next'] if 'redirect_next' in request.POST else '/'
        user_login = auth.authenticate(username=username, password=password)
        if user_login is not None:
            auth.login(request, user_login)
            # return redirect(redirect_next)
            return JsonResponse({'redirect': redirect_next})
        else:
            return JsonResponse({'error': "Username or password wrong"})
            # return redirect('/signin/')
    

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
          
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save() 
            

            # Login 
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)


            # Crete profile
            
            profile = Profile.objects.create(user=request.user)
            profile.save()



            # breakpoint()
            return JsonResponse({'redirect': True})
            # else: return redirect('/register/')
        else:
            
            return JsonResponse(errors)


class Setting(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return render(request, 'setting.html', {
            'profile': profile,
        })

    # update profile
    def post(self, request):
        user_login = request.user
        profile = Profile.objects.get(user=user_login)
        image = request.FILES.get("profile_image")
        data = request.POST.dict()
        data['user'] = user_login.id

        if image:
            # Save image to FS
            dest = f'media/profile_images/{profile.id}.jpg'
            storage.child(dest).put(image) # Save to firebase storage
            image_path = storage.child(dest).get_url(None) # Get url from firebase
            data['image_path'] = image_path
            
        
        
        # Serializer update profile
        profile_serializer = ProfileSerializer(instance=profile, data=data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return JsonResponse({'mess': 'OK'})
        else:
            return JsonResponse({'error': 'ER'})
            

class UploadPost(LoginRequiredMixin, APIView):
    login_url = 'signin' 

    def get(self, request):
        return render(request, 'home.html')
    
    def post(self, request):
        user_login = request.user
        data = request.data.dict()
        data['user'] = user_login.id
        post_serializer = PostSerializer(data=data)

        if post_serializer.is_valid():
            post_serializer = post_serializer.save() # Save post to data

            images = request.FILES.getlist('images[]')
            if images:

                for image in images:
                    id = str(uuid.uuid4())
                    dest = f'media/post_images/{id}.jpg'
                    storage.child(dest).put(image) # Save to firebase storage
                    image_path = storage.child(dest).get_url(None) # get url
              
                    # Create relationship post-image
                    post = Post.objects.get(id=post_serializer.id)
                    add_img = ImagesOfPost.objects.create(id=id, post=post, image_path=image_path)
                    add_img.save()
            
            return JsonResponse({'data': ""})
        
            
        assert False, post_serializer.errors
        # return JsonResponse({'errors': post_serializer.errors})










