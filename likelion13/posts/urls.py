from django.urls import path
from posts.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.contrib import admin
from django.urls import path, include
from posts.views import *
from accounts.views import *

from rest_framework import permissions #추가
from drf_yasg.views import get_schema_view #추가
from drf_yasg import openapi #추가

# Swagger 설정
schema_view = get_schema_view(
    openapi.Info(
        title="Post API",
        default_version="v1",
        description="게시글 API 문서",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Swagger 접근 가능하도록 설정
)

urlpatterns = [
    path('', PostList.as_view()), #post 전체 조회
    path('<int:post_id>/', PostDetail.as_view()), # post 개별 조회
    path('<int:post_id>/comment', CommentList.as_view()), #comment 전체 조회회
    path('category/<int:category_id>', CategoryList.as_view()), # 카테고리에 해당하는 Post 조회
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    # Swagger URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]