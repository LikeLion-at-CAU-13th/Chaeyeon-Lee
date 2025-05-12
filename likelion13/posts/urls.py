from django.urls import path
from posts.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [
    path('', PostList.as_view()), #post 전체 조회
    path('<int:post_id>/', PostDetail.as_view()), # post 개별 조회
    path('<int:post_id>/comment', CommentList.as_view()), #comment 전체 조회회
    path('category/<int:category_id>', CategoryList.as_view()), # 카테고리에 해당하는 Post 조회
]