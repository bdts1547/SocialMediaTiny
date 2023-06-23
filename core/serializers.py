from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validatee_data):
        user = User.objects.create_user(
            username=validatee_data['username'],
            password=validatee_data['password'],
            email=validatee_data['email']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ImageOfPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesOfPost
        fields = '__all__'


class LikeOfPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeOfPost
        fields = '__all__'


    
class CommentOfPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentOfPost
        fields = '__all__'