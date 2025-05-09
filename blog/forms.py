from django import forms
from .models import Comment, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {
            "body": "Comment",
        }
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nome")
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Mensagem")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category", "cover_image"]
        labels = {
            "title": "Title",
            "content": "Content",
            "category": "Category",
            "cover_image": "Cover Image",
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'password1', 'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user