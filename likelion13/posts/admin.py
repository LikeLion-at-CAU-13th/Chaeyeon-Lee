from django.contrib import admin
from .models import Post, Comment, Category, PostCategory

admin.site.register(Category) # Category 모델을 admin에 등록
admin.site.register(Comment)
admin.site.register(Post) # Post 모델을 admin에 등록
admin.site.register(PostCategory) # PostCategory 모델을 admin에 등록