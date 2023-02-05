from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.enums import ACCOUNT_TYPES
from gymtime_backend.settings import SMS_EXPIRATION_MINUTES
from sms.enums import SMS_USAGE_TYPES
from sms.models import SMSVerification
from utility.mixins import PhoneNumberSerializer


class SendSMSVerificationTokenSerializer(PhoneNumberSerializer):
    usage_type = serializers.ChoiceField(choices=SMS_USAGE_TYPES, write_only=True, required=False)
    account_type = serializers.ChoiceField(choices=ACCOUNT_TYPES, write_only=True)

    def validate(self, attrs):
        if SMSVerification.objects.filter(
            **attrs,
            created__gt=timezone.now() - timezone.timedelta(minutes=SMS_EXPIRATION_MINUTES)
        ).exists():
            raise ValidationError({
                'phone_number': 'بعد از ۲ دقیقه میتوانید درخواست کد جدید کنید'
            })

        return attrs

    class Meta:
        extra_kwargs = {
            'phone_number': {
                'write_only': True
            }
        }
