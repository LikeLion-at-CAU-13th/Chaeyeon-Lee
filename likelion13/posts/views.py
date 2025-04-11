from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods # 추가
from .models import *
import json

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
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "status" : post.status,
        "user" : post.user.username,
    }
    return JsonResponse({
        "status" : 200,
        "data": post_detail_json})

# 함수 데코레이터, 특정 http method만 허용
@require_http_methods(["POST", "GET"])
def post_list(request):
    
    if request.method == "POST":
    
        # byte -> 문자열 -> python 딕셔너리
        body = json.loads(request.body.decode('utf-8'))
    
		    # 프론트에게서 user id를 넘겨받는다고 가정.
		    # 외래키 필드의 경우, 객체 자체를 전달해줘야하기 때문에
        # id를 기반으로 user 객체를 조회해서 가져옵니다 !
        user_id = body.get('user')
        user = get_object_or_404(User, pk=user_id)

	    # 새로운 데이터를 DB에 생성
        new_post = Post.objects.create(
            title = body['title'],
            content = body['content'],
            status = body['status'],
            user = user
        )
    
	    # Json 형태 반환 데이터 생성
        new_post_json = {
            "id": new_post.id,
            "title" : new_post.title,
            "content": new_post.content,
            "status": new_post.status,
            "user": new_post.user.id
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json
        })
    
    # 게시글 전체 조회
    if request.method == "GET":
        post_all = Post.objects.all()
    
	# 각 데이터를 Json 형식으로 변환하여 리스트에 저장
        post_json_all = []
        
        for post in post_all:
            post_json = {
                "id": post.id,
                "title" : post.title,
                "content": post.content,
                "status": post.status,
                "user": post.user.id
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all
        })
    

@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, post_id):

    # post_id에 해당하는 단일 게시글 조회
    if request.method == "GET":
        post = get_object_or_404(Post, pk=post_id)

        post_json = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "status": post.status,
            "user": post.user.id,
        }
        
        return JsonResponse({
            'status': 200,
            'message': '게시글 단일 조회 성공',
            'data': post_json
        })
    
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        update_post = get_object_or_404(Post, pk=post_id)

        if 'title' in body:
            update_post.title = body['title']
        if 'content' in body:
            update_post.content = body['content']
        if 'status' in body:
            update_post.status = body['status']
    
        
        update_post.save()

        update_post_json = {
            "id": update_post.id,
            "title" : update_post.title,
            "content": update_post.content,
            "status": update_post.status,
            "user": update_post.user.id,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=post_id)
        delete_post.delete()

        return JsonResponse({
                'status': 200,
                'message': '게시글 삭제 성공',
                'data': None
        })
    

@require_http_methods(["GET"])
def post_comment(request, post_id):

    # post_id에 해당하는 단일 게시글 조회
    post = get_object_or_404(Post, pk=post_id)
    
    # 여러 개의 댓글을 가져오기 위해 filter 사용
    # 외래키로 연결된 Post 모델을을 통해 댓글을 가져옴
    comment_all = Comment.objects.filter(post = post_id)

    # 각 댓글을 Json 형식으로 변환하여 리스트에 저장
    comment_json_all = []
    for comment in comment_all:
        comment_json = {
            "id": comment.id,
            "content": comment.content,
            "user": comment.user,
        }
        comment_json_all.append(comment_json)

    return JsonResponse({
        'status': 200,
        'message': '댓글 목록 조회 성공',
        'data': comment_json_all
    })

@require_http_methods(["GET"])
def post_category_list(request, category_id):

    # category_id에 해당하는 단일 카테고리 조회
    category = get_object_or_404(Category, pk=category_id)
    
    # "__"로 (중간 테이블의 category 값) == (category_id)인 post 객체를 불러옴
    # order_by('created')로 생성일 기준으로 정렬
    post_all = Post.objects.filter(postcategory__category = category_id).order_by('created')

    # 각 데이터를 Json 형식으로 변환하여 리스트에 저장
    post_json_all = []
    for post in post_all:
        post_json = {
            "id": post.id,
            "title" : post.title,
            "content": post.content,
            "status": post.status,
            "user": post.user.id
        }
        post_json_all.append(post_json)

    return JsonResponse({
        'status': 200,
        'message': '카테고리별 게시글 목록 조회 성공',
        'data': post_json_all
    })