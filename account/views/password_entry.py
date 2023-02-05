from django.contrib.auth import get_user_model
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from account.jwt import get_jwt_token
from account.models import GymOwner
from account.serializers import GymOwnerPasswordLoginSerializer, GymOwnerChangePasswordSerializer, \
    GymOwnerSetPasswordSerializer


class GymOwnerPasswordLoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = GymOwnerPasswordLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        account = GymOwner.objects.all().get(phone_number=validated_data['phone_number'])
        refresh, access = get_jwt_token(account)
        return Response(data={
            'access_token': access,
            'refresh_token': refresh
        }, status=HTTP_200_OK)


class GymOwnerChangePasswordView(UpdateAPIView):
    serializer_class = GymOwnerChangePasswordSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class GymOwnerSetPasswordView(UpdateAPIView):
    serializer_class = GymOwnerSetPasswordSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user