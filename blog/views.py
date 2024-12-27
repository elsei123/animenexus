from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Category
from .forms import ContactForm, CommentForm
from .utils.emailjs_utils import send_email_via_emailjs 

def home_page(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(approved=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

def about_page(request):
    return render(request, 'blog/about.html')

def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            success = send_email_via_emailjs(name, email, message)

            if success:
                messages.success(request, 'Your message has been sent successfully!')
            else:
                messages.error(request, 'There was an error sending your message. Please try again later.')

            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

def post_list(request):
    """
    View to list posts with support for category filtering and pagination.
    """
    category_filter = request.GET.get('category', '')

    posts_list = Post.objects.all().order_by('-created_at')

    if category_filter:
        posts_list = posts_list.filter(category__name__iexact=category_filter)
    
    if not posts_list.exists():
        messages.info(request, "No posts found for the selected category.")

    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'category_filter': category_filter,
        'categories': categories
    })
