from django import forms
from .models import Comment, Post 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nome')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Mensagem')

class PostForm(forms.ModelForm):
    """
    Form for creating and editing Posts.
    """
    class Meta:
        model = Post
        # Adjust these fields according to your Post model
        fields = ['title', 'content', 'category', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Post title',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Post content',
                'class': 'form-control'
            }),
        }
