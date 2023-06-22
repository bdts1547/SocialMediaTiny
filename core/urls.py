from django.urls import path
from .views import *



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', Logout.as_view(), name='logout'),
    path('setting/', Setting.as_view(), name='setting'),
    path('upload_post/', UploadPost.as_view(), name='upload_post'),


]