from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    image_path = serializers.CharField(read_only=True, source='profile.image_path')

    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email', 'followers', 'image_path')
        extra_kwargs = {
            'followers': {'required': False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user





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
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = LikeOfPost
        fields = ('id', 'post', 'user', 'is_followed')

    
    def get_is_followed(self, user_login):
        return user_login



    
class CommentOfPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentOfPost
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'user', 'follower', 'followers', 'following']





