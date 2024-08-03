from django.urls import path
from .views import blog_view, create_blog_view, list_by_category,my_blogs

urlpatterns = [
    path('blog/<int:id>', blog_view, name='blog_view'),
    path('create-blog/', create_blog_view, name='create_blog'),
    path('my-blogs/', my_blogs, name='my_blogs'),
    path('blogs-list/<int:id>', list_by_category,name='blogs_list'),
]
