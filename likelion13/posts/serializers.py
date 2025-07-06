### Model Serializer case
from datetime import date
from rest_framework import serializers
from .models import Post
from .models import Comment
from config.custom_api_exceptions import PostConflictException, DailyPostLimitException

class PostSerializer(serializers.ModelSerializer):
  class Meta:
		# 어떤 모델을 시리얼라이즈할 건지
    model = Post
		# 모델에서 어떤 필드를 가져올지
		# 전부 가져오고 싶을 때
    fields = "__all__"
  
  def validate(self, data):
    # 중복된 게시글 제목이 있다면 예외 발생
    if Post.objects.filter(title=data['title']).exists():
      raise PostConflictException(detail=f"A post with title: '{data['title']}' already exists.")
    
    # 하루 1회 작성 제한 검사
    today = date.today()
    user = data.get('user')

    if Post.objects.filter(user=user, created__date=today).exists(): # 사용자가 오늘 작성한 게시글이 있으면
      raise DailyPostLimitException("하루에 한 번만 게시글을 작성할 수 있습니다.")

    return data

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = "__all__"

  # 14주차 과제2 - 댓글 내용이 15자 이상인지 확인하는 유효성 검사
  def validate_content(self, value):
    print("Validating comment content: ", value)
    if len(value.strip()) < 15: # strip: 앞뒤 공백 제거
      raise serializers.ValidationError("댓글은 15자 이상 작성해야 합니다다.")
    return value

from .models import Image
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"