import logging
#모든 http 요청을 로깅하는 미들웨어 클래스
logger = logging.getLogger('custom.http')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"{request.method} {request.get_full_path()}")
        response = self.get_response(request)
        return response
