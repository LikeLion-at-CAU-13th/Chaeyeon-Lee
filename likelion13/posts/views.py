from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods # 추가
from .models import *
import json

from .serializers import *
# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import *

# Create your views here.
def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello likelion-13th!"
        })
    
def index(request):
    return render(request, 'index.html')

class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, CombinedPermission]
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        posts = Post.objects.all()
        # 많은 post들을 받아오려면 (many=True) 써줘야 한다
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, CombinedPermission]
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    #put: 데이터 생성 or 전체 수정 - 호환성을 위해 사용
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(): #update이니까 유효성 검사 필요요
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

class CommentList(APIView):
    permission_classes = [TimeRestrictedPermission]
    def get(self, request, post_id):
        # post_id에 해당하는 단일 게시글 조회
        post = get_object_or_404(Post, pk=post_id)
        # 외래키로 연결된 Comment 모델을 통해 댓글을 가져와서 목록으로 저장
        comments = post.comment.all()  
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

# 카테고리별 게시글 목록 조회
class CategoryList(APIView):
    permission_classes = [TimeRestrictedPermission]
    def get(self, request, category_id):
        #category_id에 해당하는 단일 카테고리 조회
        category = get_object_or_404(Category, pk=category_id)
        #category_id에 해당하는 단일 카테고리의 postcategory를 통해 post 객체를 가져옴
        post_all = Post.objects.filter(postcategory__category=category_id).order_by('created')
        serialiazer = PostSerializer(post_all, many=True)
        return Response(serialiazer.data)
    