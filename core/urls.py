from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', Logout.as_view(), name='logout'),
    path('setting/', Setting.as_view(), name='setting'),
    path('set_profile/', SetProfile.as_view(), name='set_profile'),
    path('upload_post/', UploadPost.as_view(), name='upload_post'),
    path('edit_post/', EditPost.as_view(), name='edit_post'),
    path('delete_post/', DeletePost.as_view(), name='delete_post'),
    path('like_post/', LikePost.as_view(), name='like_post'),
    path('comment_post/', CommentPost.as_view(), name='comment_post'),
    path('dis_enable_comment/', DisEnableComment.as_view(), name='dis_enable_comment'),
    path('show_likes/<str:id>', ShowLikePost.as_view(), name='show_likes'),
    path('ban_user/', BanUser.as_view(), name='ban_user'),
    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('search/', Search.as_view(), name='search'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('test/', Test.as_view(), name='test'),



]