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
