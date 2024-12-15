from django.shortcuts import render, get_object_or_404
from .models import Post
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail


def home_page(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

def about_page(request):
    return render(request, 'blog/about.html')

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        full_message = f"Message from {name} <{email}>:\n\n{message}"
        
        send_mail(
            subject=f'New Contact Message from {name}',
            message=full_message,
            from_email='EMAIL_HOST_USER',
            recipient_list=['27zc8gmq@students.codeinstitute.net'],
        )
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    
    return render(request, 'blog/contact.html')