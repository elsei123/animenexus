from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nome')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Mensagem')
