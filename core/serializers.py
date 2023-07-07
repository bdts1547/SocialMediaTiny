from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'created_at', 'no_of_likes', 'images', 'likes', 'comments']
        extra_kwargs = {
            'images': {'required': False},
            'likes': {'required': False},
            'comments': {'required': False},
        }

 
  

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


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'user', 'follower', 'followers', 'following']