from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import redirect_to_login
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy

from .models import Post, Category, Comment,  Profile
from .forms import ContactForm, CommentForm, PostForm, SignUpForm
from .utils.emailjs_utils import send_email_via_emailjs
from django.contrib.auth import logout
from django.contrib.auth.models import User


def home(request):
    """Display homepage with paginated list of posts."""
    posts = (
        Post.objects.select_related('author', 'category')
        .all()
        .order_by('-created_at')
    )
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/home.html', {'page_obj': page_obj})


def post_list(request):
    """Display list of posts, filtered by category if provided."""
    category_name = request.GET.get('category')
    posts_qs = (
        Post.objects.select_related('author', 'category')
        .all()
        .order_by('-created_at')
    )
    if category_name:
        posts_qs = posts_qs.filter(category__name__iexact=category_name)
        if not posts_qs.exists():
            messages.info(request, f"No posts found for category '{category_name}'.")
    paginator = Paginator(posts_qs, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'category_name': category_name,
        'categories': categories,
    })


def post_detail(request, post_id):
    """Show a single post and handle comment submission."""
    post = get_object_or_404(
        Post.objects.select_related('author', 'category'),
        id=post_id
    )
    approved_comments = post.comments.filter(approved=True)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(
                request, 'Your comment has been submitted and is awaiting approval.'
            )
            return redirect(reverse('post_detail', args=[post.id]))
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': approved_comments,
        'form': form,
    })


@login_required
def create_post(request):
    """Create a new blog post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect(reverse('post_detail', args=[post.id]))
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Edit an existing post (authors only)."""
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, 'Permission denied: cannot edit this post.')
        raise Http404
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect(reverse('post_detail', args=[post.id]))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    """Delete a post after confirmation (authors only)."""
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, 'Permission denied: cannot delete this post.')
        raise Http404
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect(reverse('post_list'))
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def edit_comment(request, comment_id):
    """Edit a comment (authors only)."""
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, 'Permission denied: cannot edit this comment.')
        raise Http404
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect(reverse('post_detail', args=[comment.post.id]))
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {
       'form': form,
       'comment': comment,
    })


@login_required
def delete_comment(request, comment_id):
    """Delete a comment after confirmation (owners only)."""
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, 'Permission denied: cannot delete this comment.')
        raise Http404
    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect(reverse('post_detail', args=[post_id]))
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})


@login_required
def profile(request, username=None):
    """Render user profile page, creating Profile if missing."""
    if username:
         user_obj = get_object_or_404(User, username=username)
    else:
         user_obj = request.user

    profile_obj, created = Profile.objects.get_or_create(user=user_obj)
    return render(request, 'blog/profile.html', {'profile': profile_obj})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You logout")
    return redirect('post_list')


def about(request):
    """Render static About page."""
    return render(request, 'blog/about.html')


def contact(request):
    """Render and process Contact form via EmailJS."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            success = send_email_via_emailjs(
                data['name'], data['email'], data['message']
            )
            if success:
                messages.success(request, 'Message sent successfully.')
            else:
                messages.error(
                    request, 'Failed to send message;please try again later.'
                )
            return redirect(reverse_lazy('contact'))
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


def signup(request):
    """Handle user signup and auto-login."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(
                request, f"Welcome, {user.username}! Your account has been created."
            )
            return redirect(reverse('post_list'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

    if username:
        user = get_object_or_404(User, username=username)
    else:
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user

    return render(request, 'blog/profile.html', {'profile': user.profile})
