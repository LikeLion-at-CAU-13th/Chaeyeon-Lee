from django.urls import path
from posts.views import *

urlpatterns = [
    #path('', hello_world, name = 'hello_world'),
    #path('page', index, name = 'my-page'),
    #path('<int:id>', get_post_detail) # 추가

    #path('', post_list, name="post_list"),
    #path('<int:post_id>', post_detail, name="post_detail"),  #Post 단일 조회
    path('', PostList.as_view()), #post 전체 조회회
    path('<int:post_id>/', PostDetail.as_view()), # post 개별 조회
    path('<int:post_id>/comment', CommentList.as_view()), #comment 전체 조회회
    #path('<int:post_id>/comment', post_comment, name="post_comment"), # Post 댓글 조회
    path('category/<int:category_id>', post_category_list, name="post_category_list"), # 카테고리에 해당하는 Post 조회
]