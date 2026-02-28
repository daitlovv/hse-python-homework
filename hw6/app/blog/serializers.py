from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_id', 'created_at', 'updated_at', 'likes', 'total_likes']
        read_only_fields = ['created_at', 'updated_at', 'likes']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    post_id = serializers.IntegerField(write_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_id', 'author', 'author_id', 'content','created_at', 'updated_at', 'likes', 'total_likes', 'parent']
        read_only_fields = ['created_at', 'updated_at', 'likes']