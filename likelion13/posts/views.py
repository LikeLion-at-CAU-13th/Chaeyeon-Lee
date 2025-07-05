from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods

from config.custom_exceptions import * # 커스텀 예외 import 추가
from .models import *
import json

from .serializers import *
# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import *

from django.core.files.storage import default_storage  
from .serializers import ImageSerializer
from django.conf import settings
import boto3
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid # 파일 중복 업로드 위해 import

# Create your views here.
def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello likelion-13th!"
        })
    
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def get_post_detail(reqeust, id):
    try:
        post = Post.objects.get(id=id)
        post_detail_json = {
            "id" : post.id,
            "title" : post.title,
            "content" : post.content,
            "status" : post.status,
            "user" : post.user.username
        }
        return JsonResponse({
            "status" : 200,
            "data": post_detail_json})
    except Post.DoesNotExist:
        raise PostNotFoundException

class PostList(APIView):
    @swagger_auto_schema(
        operation_summary="게시글 생성",
        operation_description="새로운 게시글을 생성합니다.",
        request_body=PostSerializer,
        responses={201: PostSerializer, 400: "잘못된 요청"}
    )
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # raise_exception=True로 설정하면 유효성 검사 실패 시 예외 발생
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="게시글 목록 조회",
        operation_description="모든 게시글을 조회합니다.",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, format=None):
        posts = Post.objects.all()
	    # 많은 post들을 받아오려면 (many=True) 써줘야 한다!
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
     
class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, CombinedPermission]
    
    @swagger_auto_schema(
        operation_summary="단일 게시글 조회",
        operation_description="post_id에 해당하는 게시글을 조회합니다.",
        responses={200: PostSerializer}
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="게시글 수정",
        operation_description="post_id에 해당하는 게시글을 수정합니다.",
        request_body=PostSerializer,
        responses={200: PostSerializer, 400: "잘못된 요청"}
    )
    #put: 데이터 생성 or 전체 수정 - 호환성을 위해 사용
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(): #update이니까 유효성 검사 필요요
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="게시글 삭제",
        operation_description="post_id에 해당하는 게시글을 삭제합니다.",
        responses={204: "삭제 성공", 404: "존재하지 않음"}
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

class CommentList(APIView):
    permission_classes = [TimeRestrictedPermission]
    
    @swagger_auto_schema(
        operation_summary="게시글 댓글 목록 조회",
        operation_description="post_id에 해당하는 게시글의 댓글들을 조회합니다.",
        responses={200: CommentSerializer(many=True)}
    )
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

    @swagger_auto_schema(
        operation_summary="카테고리별 게시글 목록 조회",
        operation_description="category_id에 해당하는 카테고리의 게시글들을 조회합니다.",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, category_id):
        #category_id에 해당하는 단일 카테고리 조회
        category = get_object_or_404(Category, pk=category_id)
        #category_id에 해당하는 단일 카테고리의 postcategory를 통해 post 객체를 가져옴
        post_all = Post.objects.filter(postcategory__category=category_id).order_by('created')
        serialiazer = PostSerializer(post_all, many=True)
        return Response(serialiazer.data)
    
class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # form-data 테스트를 위한 파서
    @swagger_auto_schema(
        operation_summary="이미지 업로드",
        operation_description="S3에 이미지를 업로드하고 해당 URL을 반환합니다.",
        manual_parameters=[
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='업로드할 이미지 파일'
            )
        ],
        responses={201: ImageSerializer}
    )
    def post(self, request):
        print("요청 도착")
        if 'image' not in request.FILES:
            print("이미지 없음")
            return Response({"error": "No image file"}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # S3에 파일 저장
        # 파일 확장자 유지
        extension = image_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{extension}"
        file_path = f"uploads/{unique_filename}"
        
        # S3에 파일 업로드
        try:
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path,
                Body=image_file.read(),
                ContentType=image_file.content_type,
            )
        except Exception as e:
            return Response({"error": f"S3 Upload Failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 업로드된 파일의 URL 생성
        image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file_path}"

        # DB에 저장
        image_instance = Image.objects.create(image_url=image_url)
        serializer = ImageSerializer(image_instance)


        return Response(serializer.data, status=status.HTTP_201_CREATED)