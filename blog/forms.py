from django import forms
from .models import Comment, Post 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': 'Comment',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nome')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Mensagem')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'cover_image']
        labels = {
            'title': 'Title',
            'content': 'Content',
            'category': 'Category',
            'cover_image': 'Cover Image',
        }
