from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib import messages


@receiver(user_logged_in)
def welcome_message(sender, request, user, **kwargs):
    """
    Send a welcome message when a user logs in.
    Triggered by Django's built-in user_logged_in signal.
    """
    messages.success(request, f"Welcome back, {user.username}! 🎉")


@receiver(user_logged_out)
def goodbye_message(sender, request, user, **kwargs):
    """
    Send a goodbye message when a user logs out.
    """
    messages.info(request, "You have been logged out. See you soon! 👋")
