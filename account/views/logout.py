from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.status import HTTP_418_IM_A_TEAPOT
from rest_framework.views import APIView


class AccountLogout(APIView):
    """
    This Functionality should be implemented whenever the "BlackList" option is
    enabled in JWT config.
    """
    def get(self, request, *args, **kwargs):
        return Response({"message": "ok"}, status=HTTP_418_IM_A_TEAPOT)
