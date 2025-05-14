from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post, Profile


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments.
    """
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": "Comment"}
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4, "placeholder": "Write your comment here..."})
        }


class ContactForm(forms.Form):
    """
    Simple contact form for users to send messages.
    """
    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(attrs={"placeholder": "Your full name"})
    )
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"})
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Type your message here"})
    )


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.
    """
    class Meta:
        model = Post
        fields = ["title", "content", "category", "cover_image"]
        labels = {
            "title": "Post Title",
            "content": "Content",
            "category": "Category",
            "cover_image": "Cover Image (optional)",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter post title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post content"}),
        }


class SignUpForm(UserCreationForm):
    """
    User registration form extending Django's built-in UserCreationForm.
    """
    email = forms.EmailField(
        required=True,
        label="Email address",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First name",
        widget=forms.TextInput(attrs={"placeholder": "First name"})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last name",
        widget=forms.TextInput(attrs={"placeholder": "Last name"})
    )
    date_of_birth = forms.DateField(
        required=True,
        label="Date of birth",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data["date_of_birth"]
            )
        return user
