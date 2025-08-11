from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, Comment, Post, Profile


class BlogTests(TestCase):
    def setUp(self):
        # create two users
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass456")
        # create category
        self.cat = Category.objects.create(name="TestCat")
        # create a post by user1
        self.post = Post.objects.create(
            title="Test Title", content="Test content", author=self.user1, category=self.cat
        )
        self.client = Client()

    def test_create_post_requires_login(self):
        url = reverse("create_post")
        resp = self.client.get(url)
        # without login, should redirect to /accounts/login/
        self.assertRedirects(resp, f"/accounts/login/?next={url}")

    def test_create_post_success(self):
        self.client.login(username="user1", password="pass123")
        url = reverse("create_post")
        data = {
            "title": "New Post",
            "content": "Content",
            "category": self.cat.id,
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Post.objects.filter(title="New Post").exists())
        messages = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertIn("Post created successfully.", messages)

    def test_edit_post_permission(self):
        # user2 tries to edit user1's post
        self.client.login(username="user2", password="pass456")
        url = reverse("edit_post", kwargs={"post_id": self.post.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_delete_post(self):
        self.client.login(username="user1", password="pass123")
        url = reverse("delete_post", kwargs={"post_id": self.post.id})
        # GET shows confirmation; POST deletes
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)
        resp_post = self.client.post(url, follow=True)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
        messages = [m.message for m in get_messages(resp_post.wsgi_request)]
        self.assertIn("Post deleted successfully.", messages)

    def test_comment_creation_requires_login(self):
        # only registered users should be allowed to post comments
        url = reverse("post_detail", kwargs={"post_id": self.post.id})
        resp = self.client.post(url, {"body": "Test"}, follow=True)
        login_url = reverse("login")
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(resp, expected_redirect, fetch_redirect_response=False)

    def test_post_detail_get_and_context(self):
        url = reverse("post_detail", kwargs={"post_id": self.post.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["post"], self.post)
        self.assertIn("form", resp.context)
        self.assertEqual(list(resp.context["comments"]), [])

    def test_edit_comment_get_and_post(self):
        comment = Comment.objects.create(post=self.post, user=self.user1, body="Olá", approved=True)
        url = reverse("edit_comment", kwargs={"comment_id": comment.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username="user1", password="pass123")
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)
        resp_post = self.client.post(url, {"body": "Editado"}, follow=True)
        comment.refresh_from_db()
        self.assertEqual(comment.body, "Editado")
        messages = [m.message for m in get_messages(resp_post.wsgi_request)]
        self.assertIn("Comment updated successfully.", messages)

    def test_delete_comment_get_and_post(self):
        comment = Comment.objects.create(post=self.post, user=self.user1, body="Para apagar", approved=True)
        url = reverse("delete_comment", kwargs={"comment_id": comment.id})
        self.client.login(username="user1", password="pass123")
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)
        resp_post = self.client.post(url, follow=True)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
        messages = [m.message for m in get_messages(resp_post.wsgi_request)]
        self.assertIn("Comment deleted successfully.", messages)

    def test_signup_creates_user_profile_and_logs_in(self):
        url = reverse("signup")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "date_of_birth": "1990-01-01",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        resp = self.client.post(url, data, follow=True)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(Profile.objects.filter(user__username="newuser").exists())
        self.assertTrue(resp.wsgi_request.user.is_authenticated)
        messages = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertIn("Welcome, newuser! Your account has been created.", messages)

    @patch("blog.views.send_email_via_emailjs")
    def test_contact_form_success_and_failure(self, mock_send):
        url = reverse("contact")
        mock_send.return_value = True
        data = {"name": "Test", "email": "t@e.com", "message": "Olá"}
        resp_sucesso = self.client.post(url, data, follow=True)
        msgs = [m.message for m in get_messages(resp_sucesso.wsgi_request)]
        self.assertIn("Message sent successfully.", msgs)
        mock_send.return_value = False
        resp_falha = self.client.post(url, data, follow=True)
        msgs = [m.message for m in get_messages(resp_falha.wsgi_request)]
        self.assertIn("Failed to send message;please try again later.", msgs)

    def test_profile_view_own_and_other(self):
        self.client.login(username="user1", password="pass123")
        url_own = reverse("profile")
        resp_own = self.client.get(url_own)
        self.assertEqual(resp_own.status_code, 200)
        self.assertEqual(resp_own.context["profile"].user, self.user1)
        Profile.objects.create(user=self.user2)
        url_other = reverse("profile", kwargs={"username": "user2"})
        resp_other = self.client.get(url_other)
        self.assertEqual(resp_other.status_code, 200)
        self.assertEqual(resp_other.context["profile"].user, self.user2)
