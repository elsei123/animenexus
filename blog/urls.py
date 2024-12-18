from django.urls import path
from .views import home_page, post_detail, about_page, contact_page, post_list

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
]

