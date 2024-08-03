from django.contrib import admin
from .models import BlogPost, Category
from django.contrib.auth.admin import UserAdmin


admin.site.register(BlogPost)
admin.site.register(Category)