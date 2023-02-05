from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from account.jwt import get_jwt_token
from account.models import Account, Athlete, GymOwner
from account.serializers.sms_entry_v2 import AthleteLoginSerializerV2, AthleteSignupSerializerV2, \
    GymOwnerLoginSerializerV2, GymOwnerSignUpSerializerV2
from sms.enums import SMS_USAGE_TYPE_LOGIN, SMS_USAGE_TYPE_SIGNUP
from sms.models import SMSVerification
from utility.mixins import PhoneNumberSerializer


class BaseAccountSMSEntryViewV2(APIView):
    queryset = None
    login_serializer_class = None
    signup_serializer_class = None

    @staticmethod
    def mark_token_as_used_with_usage(serializer, usage_type):
        SMSVerification.mark_token_as_used(
            phone_number=serializer.validated_data['phone_number'],
            token=serializer.context['sms_token'],
            usage_type=usage_type
        )

    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            account = self.queryset.get(phone_number=serializer.validated_data.get('phone_number'))
            serializer = self.login_serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            sms_usage_type = SMS_USAGE_TYPE_LOGIN
        except Account.DoesNotExist as e:
            serializer = self.signup_serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            sms_usage_type = SMS_USAGE_TYPE_SIGNUP

        self.mark_token_as_used_with_usage(serializer, sms_usage_type)
        refresh, access = get_jwt_token(account)
        return Response(
            data={
                'access_token': access,
                'refresh_token': refresh,
                'is_sign_up': sms_usage_type == SMS_USAGE_TYPE_SIGNUP
            },
            status=HTTP_200_OK
        )


class AthleteSMSEntryViewV2(BaseAccountSMSEntryViewV2):
    queryset = Athlete.objects.all()
    login_serializer_class = AthleteLoginSerializerV2
    signup_serializer_class = AthleteSignupSerializerV2


class GymOwnerSMSEntryViewV2(BaseAccountSMSEntryViewV2):
    queryset = GymOwner.objects.all()
    login_serializer_class = GymOwnerLoginSerializerV2
    signup_serializer_class = GymOwnerSignUpSerializerV2
