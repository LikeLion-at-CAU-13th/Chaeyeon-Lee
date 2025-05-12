from rest_framework.permissions import BasePermission
import datetime

#특정 시간대에만 게시판을 이용할 수 있도록 제한하는 권한
class TimeRestrictedPermission(BasePermission):
    message = "이 시간대에는 게시판을 이용할 수 없습니다 (오전 7시 ~ 오후 10시만 가능)."

    def has_permission(self, request, view):
        now = datetime.datetime.now().time()
        # 금지 시간: 22:00 ~ 다음날 07:00
        if now >= datetime.time(22, 0) or now <= datetime.time(7, 0):
            return False
        return True

# 게시글 작성자만 수정 및 삭제 가능하도록 하는 권한
class IsOwnerOrReadOnly(BasePermission):
    message = "작성자만 수정 및 삭제가 가능합니다."

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS 요청은 모두 허용
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # 수정/삭제는 작성자만 가능
        return obj.user == request.user

class CombinedPermission(TimeRestrictedPermission, IsOwnerOrReadOnly):
    """
    두 개의 권한을 동시에 적용:
    1) 시간 제한 검사 (has_permission)
    2) 작성자만 수정/삭제 허용 (has_object_permission)
    """
    pass
