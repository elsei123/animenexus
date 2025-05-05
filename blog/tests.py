from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Category

from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Category, Post

class BlogTests(TestCase):
    def setUp(self):
        # create two users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass456')
        # create category
        self.cat = Category.objects.create(name='TestCat')
        # create a post by user1
        self.post = Post.objects.create(
            title='Test Title',
            body='Test content',
            author=self.user1,
            category=self.cat
        )
        self.client = Client()

    def test_create_post_requires_login(self):
        url = reverse('create_post')
        resp = self.client.get(url)
        # without login, should redirect to /accounts/login/
        self.assertRedirects(resp, f"/accounts/login/?next={url}")

    def test_create_post_success(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('create_post')
        data = {
            'title': 'New Post',
            'body': 'Content',
            'category': self.cat.id,
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Post.objects.filter(title='New Post').exists())
        # success message
        messages = list(resp.context['messages'])
        self.assertIn('Post created successfully!', [m.message for m in messages])

    def test_edit_post_permission(self):
        # user2 tries to edit user1's post
        self.client.login(username='user2', password='pass456')
        url = reverse('edit_post', kwargs={'post_id': self.post.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_delete_post(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('delete_post', kwargs={'post_id': self.post.id})
        # GET shows confirmation; POST deletes
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)
        resp_post = self.client.post(url, follow=True)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
        messages = [m.message for m in resp_post.context['messages']]
        self.assertIn('Post deleted successfully!', messages)
