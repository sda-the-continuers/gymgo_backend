from account.enums import ACCOUNT_TYPE_GYM_OWNER
from account.models import Account, PhoneNumberMixin
from django.db import models


class GymOwner(PhoneNumberMixin, Account):
    default_account_type = ACCOUNT_TYPE_GYM_OWNER

    shaba = models.CharField(
        max_length=32,
        verbose_name='شماره شبا',
        null=True,
        blank=True
    )

    @staticmethod
    def construct_user_key(phone_number):
        return f'{GymOwner.default_account_type}-{phone_number}'

    class Meta:
        verbose_name = 'صاحب ورزشگاه'
        verbose_name_plural = 'صاحبان ورزشگاه'
