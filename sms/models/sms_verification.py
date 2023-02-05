from django.db import models
from django.utils import timezone
from rest_framework.generics import get_object_or_404

from account.enums import ACCOUNT_TYPES
from gymtime_backend import settings
from gymtime_backend.settings import SMS_EXPIRATION_MINUTES, KAVENEGAR_VERIFY_TEMPLATE
from sms.enums import SMS_USAGE_TYPES
from sms.models import GymtimeLookupSMS
from utility.random import generate_random_number


def generate_token():
    return generate_random_number(settings.SMS_VERIFICATION_CODE_LENGTH)


class SMSVerification(GymtimeLookupSMS):

    token = models.CharField(
        max_length=8,
        default=generate_token,
        verbose_name='کد'
    )

    usage_type = models.CharField(
        choices=SMS_USAGE_TYPES,
        max_length=16,
        verbose_name='منظور استفاده'
    )

    account_type = models.CharField(
        choices=ACCOUNT_TYPES,
        max_length=16,
        verbose_name='نوع اکانت'
    )

    is_used = models.BooleanField(
        default=False,
        verbose_name='استفاده شده؟'
    )

    template = KAVENEGAR_VERIFY_TEMPLATE

    @classmethod
    def mark_token_as_used(cls, phone_number, token, usage_type):
        sms_obj = get_object_or_404(
            cls.objects.all(),
            phone_number=phone_number,
            token=token,
            created__gt=timezone.now() - timezone.timedelta(minutes=SMS_EXPIRATION_MINUTES)
        )
        sms_obj.is_used = True
        sms_obj.usage_type = usage_type
        sms_obj.save(update_fields=['is_used', 'usage_type'])

    def get_tokens(self):
        return [self.token]

    class Meta:
        verbose_name = 'تایید صلاحیت SMS'
        verbose_name_plural = 'تایید صلاحیت SMS'

