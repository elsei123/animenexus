from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import redirect_to_login
from django.core.paginator import Paginator

from .models import Post, Category, Comment
from .forms import ContactForm, CommentForm, PostForm, SignUpForm
from .utils.emailjs_utils import send_email_via_emailjs


def home(request):
    """Homepage: list all posts with pagination."""
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/home.html", {"page_obj": page_obj})


def post_list(request):
    category_filter = request.GET.get('category', '')
    posts_list = Post.objects.all().order_by('-created_at')

    if category_filter:
        posts_list = posts_list.filter(category__name__iexact=category_filter)
        if not posts_list.exists():
            messages.info(request, f"No posts found in category “{category_filter}”.")
    
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'category_filter': category_filter,
        'categories': categories,
    })


def post_detail(request, post_id):
    """Detail view: show a single post and handle new comments."""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(approved=True)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment is awaiting approval.")
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
    })


@login_required
def create_post(request):
    """Create a new blog post."""
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully.")
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {"form": form})


@login_required
def edit_post(request, post_id):
    """Edit an existing post (only author can)."""
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, "You do not have permission to edit this post.")
        raise Http404

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {"form": form, "post": post})


@login_required
def delete_post(request, post_id):
    """Delete a post after confirmation (only author can)."""
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, "You do not have permission to delete this post.")
        raise Http404

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("post_list")

    return render(request, "blog/post_confirm_delete.html", {"post": post})


@login_required
def edit_comment(request, comment_id):
    """Edit a comment (only comment owner can)."""
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, "You do not have permission to edit this comment.")
        raise Http404

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect("post_detail", post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, "blog/comment_form.html", {"form": form})


@login_required
def delete_comment(request, comment_id):
    """Delete a comment after confirmation (only owner can)."""
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, "You do not have permission to delete this comment.")
        raise Http404

    if request.method == "POST":
        post_id = comment.post.id
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect("post_detail", post_id=post_id)

    return render(request, "blog/comment_confirm_delete.html", {"comment": comment})

@login_required
def profile(request):
    """Render user profile page."""
    return render(request, 'blog/profile.html')


def about(request):
    """Static about page."""
    return render(request, "blog/about.html")


def contact(request):
    """Contact form page using EmailJS."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            success = send_email_via_emailjs(name, email, message)

            if success:
                messages.success(request, "Your message has been sent.")
            else:
                messages.error(request, "Error sending message. Please try again later.")

            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "blog/contact.html", {"form": form})


def signup(request):
    """User registration view."""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account was created.")
            return redirect("post_list")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


def about_page(request):
    """Render the About page."""
    return render(request, 'blog/about.html')


def contact_page(request):
    """Render the Contact page."""
    return render(request, 'blog/contact.html')