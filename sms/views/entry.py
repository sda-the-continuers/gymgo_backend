from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from sms.enums import GYMTIME_SMS_SENT
from sms.models import SMSVerification
from sms.serializers import SendSMSVerificationTokenSerializer


class SendSMSVerificationTokenView(APIView):

    def post(self, request):
        serializer = SendSMSVerificationTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        sms_obj = SMSVerification.objects.create(**validated_data)
        sms_obj.validate_and_send(save=True)
        if sms_obj.state == GYMTIME_SMS_SENT:
            return Response(status=HTTP_200_OK)
        raise ValidationError(str(sms_obj.gymtime_errors))
