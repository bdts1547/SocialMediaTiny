from django.urls import path
from .views import *



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', Logout.as_view(), name='logout'),
    path('setting/', Setting.as_view(), name='setting'),
    path('upload_post/', UploadPost.as_view(), name='upload_post'),
    path('delete_post/', DeletePost.as_view(), name='delete_post'),
    path('like_post/', LikePost.as_view(), name='like_post'),
    path('comment_post/', CommentPost.as_view(), name='comment_post'),
    path('show_likes/<str:id>', ShowLikePost.as_view(), name='show_likes'),
    path('ban_user/', BanUser.as_view(), name='ban_user'),


    path('test/', Test.as_view(), name='test'),



]