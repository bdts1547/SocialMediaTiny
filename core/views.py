from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
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
        list_profiles, list_images = [], []
        list_comments, list_user_likes = [], []
        for post in list_posts:
            # Profile of host post
            profile = Profile.objects.get(user=post.user)
            list_profiles.append(profile)
            
            # List images of posts
            list_image_post = ImagesOfPost.objects.filter(post=post)
            list_images.append(list_image_post)

            # List user-like of posts
            # list_no_like_post = LikeOfPost.objects.filter(post=post)
            user_liked_post = True if LikeOfPost.objects.filter(post=post, user=request.user).exists() else False
            list_user_likes.append(user_liked_post)

            # List profile-comments of posts
            list_comment_post = CommentOfPost.objects.filter(post=post)
            list_comments.append(list_comment_post)
        
        zip_data = zip(list_posts, list_profiles, list_images, list_comments, list_user_likes)
        return render(request, 'home.html', {
            'profile_login': profile_login,
            'zip_data': zip_data,
            'test': 'test',
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
        errors = check_error_accout(username, email, password, password2)

        if not errors: 
          
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save() 
            

            # Login 
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)


            # Create profile
            profile = Profile.objects.create(user=request.user)
            profile.save()

            return JsonResponse({'redirect': True})
  
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
            return JsonResponse({'redirect': '/setting'})
        else:
            return JsonResponse({'error': 'ER'})


class UploadPost(LoginRequiredMixin, PermissionRequiredMixin, APIView):
    login_url = 'signin'
    permission_required = ['core.add_post']

    def handle_no_permission(self):
        # Customize the behavior when the user doesn't have the required permission
        raise PermissionDenied("You don't have permission")

    def get(self, request):
        return render(request, 'home.html')
    
    def post(self, request):
        user_login = request.user
        data = request.data.dict()
        data['user'] = user_login.id
        post_serializer = PostSerializer(data=data)
       
        if post_serializer.is_valid():
            post = post_serializer.save() # Save post to data
            images = request.FILES.getlist('images[]')
            if images:
                for image in images:
                    save_image_post_to_firebase(storage, image, post)
                    # id = str(uuid.uuid4())
                    # dest = f'media/post_images/{id}.jpg'
                    # storage.child(dest).put(image) # Save to firebase storage
                    # image_path = storage.child(dest).get_url(None) # get url
              
                    # # Create relationship post-image
                    # add_img = ImagesOfPost.objects.create(id=id, post=post, image_path=image_path)
                    # add_img.save()


            post_updated = Post.objects.get(id=post.id)
            post_json = PostSerializer(post_updated).data
            path_images = [image.image_path for image in post_updated.images.all()]
            # breakpoint()
            return JsonResponse(post_json)
        
            
        assert False, post_serializer.errors
        # return JsonResponse({'errors': post_serializer.errors})


class EditPost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        id_post = request.GET['id_post']
        post = Post.objects.get(id=id_post)
        path_images = [image.image_path for image in post.images.all()]
        
        return JsonResponse({
            'username': post.user.username,
            'profile_image': post.user.profile.image_path,
            'title': post.title,
            'images_url': path_images,
        })

    def post(self, request):
        id_post = request.POST['id']
        title = request.POST['title']
        images = request.FILES.getlist('new_images')
        post = Post.objects.get(id=id_post)

        # Change images
        try:
            old_current_images_path = request.POST.getlist('old_images')
            old_images = post.images.all()
            for img in old_images:
                if img.image_path not in old_current_images_path:
                    img.delete()
        except: pass
        if images:
            for image in images:
                save_image_post_to_firebase(storage, image, post)
            
        post.title = title
        post.save()

        post = Post.objects.get(id=post.id)
        path_images = [image.image_path for image in post.images.all()]
        return JsonResponse({
            'id': post.id,
            'title': title,
            'path_images': path_images,
        })


class DeletePost(LoginRequiredMixin, View):
    login_url = 'signin'
 

    def post(self, request):
        id_post = request.POST['id_post']
        post = Post.objects.filter(id=id_post).first()
    
        if post and (post.user == request.user or request.user.has_perm('core.delete_post')):
            post.delete()
            return JsonResponse({'is_deleted': True})
        else:
            assert False, "No post to delete"
            return JsonResponse({'is_deleted': False})


class LikePost(LoginRequiredMixin, View):
    def get(self, request):
        user_login = request.user
        id_post = request.GET['id_post']
        post = Post.objects.get(id=id_post)
        is_liked = True
        try:
            liked = LikeOfPost.objects.get(user=user_login, post=post)
            is_liked = False
            liked.delete()

            post.no_of_likes -= 1
            post.save()
        except:
            new_like = LikeOfPost.objects.create(user=user_login, post=post)
            new_like.save()

            post.no_of_likes += 1
            post.save()

        return JsonResponse({
            'is_liked': is_liked,
            'id_post': id_post,
            })


class CommentPost(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        id_post = request.POST['id_post']
        comment = request.POST['comment']
        user_login = request.user
        post = Post.objects.get(id=id_post)
        # breakpoint()
        
        new_comment = CommentOfPost.objects.create(post=post, user=user_login, comment=comment)
        new_comment.save()

        post.no_of_comments += 1
        post.save()


        return JsonResponse({
            'comment': comment,
            'username': user_login.username, 
            'image_path': user_login.profile.image_path,
            })


class ShowLikePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, id):
        post = Post.objects.get(id=id)
        likes = LikeOfPost.objects.filter(post=post)
        data = []
        for like in likes:
            data.append({
                'username': like.user.username,
                'image_path': like.user.profile.image_path,
                'is_followed': False,
            })

        # username, image_path, follower
        return JsonResponse({
            'data': data,
        })
    

class BanUser(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request):
        id_user_ban = request.POST['id_user_ban']
        id_user_unban = request.POST['id_user_unban']

        user_ban = User.objects.filter(id=id_user_ban).first()
        user_unban = User.objects.filter(id=id_user_unban).first()

        if user_ban and not user_ban.is_staff and request.user.is_staff:
            try:
                default_gr = Group.objects.get(name='default')
                default_gr.user_set.remove(user_ban)
            except: pass
            
            try:
                mod_gr = Group.objects.get(name='mod')
                mod_gr.user_set.remove(user_ban)
            except: pass
            
    
            return JsonResponse({'type': 'ban'})
        
        if user_unban and request.user.is_staff:
            try:
                default_gr = Group.objects.get(name='default')
                default_gr.user_set.add(user_unban)
            except: pass
      

            return JsonResponse({'type': 'unban'})

        assert False, "JsonResponse({'success': False})"

        

        






class Test(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request):
        breakpoint()

    def post(self, request):
        pass


