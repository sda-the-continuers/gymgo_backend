from abc import abstractmethod

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from account.jwt import get_jwt_token
from account.models import Athlete, GymOwner
from account.serializers import AthleteLoginSerializer, AthleteSignupSerializer, GymOwnerLoginSerializer, \
    GymOwnerSignUpSerializer
from sms.models import SMSVerification


class BaseAccountSMSEntryView(APIView):
    queryset = None
    serializer = None

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        return self.serializer

    @abstractmethod
    def post(self, request, *args, **kwargs):
        pass


class BaseAccountSMSLoginView(BaseAccountSMSEntryView):

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        account = self.get_queryset().get(phone_number=validated_data.get('phone_number'))
        SMSVerification.mark_token_as_used(
            phone_number=serializer.validated_data['phone_number'],
            token=serializer.context['sms_token']
        )
        refresh, access = get_jwt_token(account)
        return Response(data={
            'access': access,
            'refresh': refresh
        }, status=HTTP_200_OK)


class BaseAccountSMSSignUpView(BaseAccountSMSEntryView):

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        SMSVerification.mark_token_as_used(
            phone_number=serializer.validated_data['phone_number'],
            token=serializer.context['sms_token']
        )
        refresh, access = get_jwt_token(account)
        return Response(data={
            'access_token': access,
            'refresh_token': refresh
        }, status=HTTP_200_OK)


class AthleteSMSLoginView(BaseAccountSMSLoginView):
    queryset = Athlete.objects.all()
    serializer = AthleteLoginSerializer


class AthleteSMSSignupView(BaseAccountSMSSignUpView):
    queryset = Athlete.objects.all()
    serializer = AthleteSignupSerializer


class GymOwnerSMSLoginView(BaseAccountSMSLoginView):
    queryset = GymOwner.objects.all()
    serializer = GymOwnerLoginSerializer


class GymOwnerSMSSignupView(BaseAccountSMSSignUpView):
    queryset = Athlete.objects.all()
    serializer = GymOwnerSignUpSerializer


