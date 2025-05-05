from django.urls import path
from .views import post_detail, about_page, contact_page, post_list

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

]

