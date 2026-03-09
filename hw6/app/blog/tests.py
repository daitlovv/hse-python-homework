from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Post, Comment

class PostCommentAPITestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='like123!')
        self.user2 = User.objects.create_user(username='user2', password='like123!')
        
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Здорово',
            author=self.user1
        )
        
        self.comment = Comment.objects.create(
            post=self.post,
            content='Кайф',
            author=self.user1
        )
        
        self.client = APIClient()

    def test_list_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_unauthorized(self):
        data = {'title': 'Новый пост', 'content': 'Котята тут'}
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_authorized(self):
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Новый пост', 'content': 'Тут такоое', 'author_id': self.user1.id}
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_update_post_as_author(self):
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Обновленный заголовок'}
        response = self.client.patch(f'/api/posts/{self.post.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Обновленный заголовок')

    def test_update_post_as_other_user(self):
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Попытка взлома'}
        response = self.client.patch(f'/api/posts/{self.post.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_as_author(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_like_post(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['liked'])

    def test_create_comment_authorized(self):
        self.client.force_authenticate(user=self.user2)
        data = {
            'content': 'Зашквар', 
            'post_id': self.post.id,
            'author_id': self.user2.id
        }
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_top_posts(self):
        response = self.client.get('/api/posts/top/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment_as_author(self):
        self.client.force_authenticate(user=self.user1)
        data = {'content': 'Обновленный комментарий'}
        response = self.client.patch(f'/api/comments/{self.comment.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Обновленный комментарий')

    def test_update_comment_as_other_user(self):
        self.client.force_authenticate(user=self.user2)
        data = {'content': 'Попытка взлома комментария'}
        response = self.client.patch(f'/api/comments/{self.comment.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_as_author(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_like_comment(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/comments/{self.comment.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['liked'])