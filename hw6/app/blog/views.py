from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        author = User.objects.get(id=self.request.data.get('author_id'))
        serializer.save(author=author)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = User.objects.get(id=request.data.get('user_id'))
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        return Response({'liked': liked, 'total_likes': post.likes.count()})
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        top_posts = Post.objects.annotate(
            comments_count=Count('comments')
        ).order_by('-comments_count')[:5]
        serializer = self.get_serializer(top_posts, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        author = User.objects.get(id=self.request.data.get('author_id'))
        serializer.save(author=author)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = User.objects.get(id=request.data.get('user_id'))
        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True
        return Response({'liked': liked, 'total_likes': comment.likes.count()})

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer