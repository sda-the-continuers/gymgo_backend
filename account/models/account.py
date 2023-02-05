from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from account.enums import ACCOUNT_TYPES
from account.jwt import JWTAccountInterface
from utility.models import HistoricalBaseModel


class Account(JWTAccountInterface, HistoricalBaseModel):

    full_name = models.CharField(
        max_length=256,
        verbose_name='نام کامل',
        null=True, blank=True
    )

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        related_name='account',
        on_delete=models.PROTECT,
        verbose_name='یوزر جنگو'
    )

    wallet = models.OneToOneField(
        to='financial.Wallet',
        related_name='account',
        on_delete=models.PROTECT,
        verbose_name='کیف پول'
    )

    crm_account = models.OneToOneField(
        to='crm.CRMAccount',
        related_name='account',
        on_delete=models.PROTECT,
        verbose_name='حساب کاربری سی‌آرام'
    )

    account_type = models.CharField(
        max_length=128,
        choices=ACCOUNT_TYPES,
        verbose_name='نوع حساب کاربری',
    )

    @property
    def profile_picture(self):
        return self.profile_pictures.exclude(is_active=False).order_by('id').last()

    default_account_type: str = None

    def get_default_account_type(self):
        if self.default_account_type not in dict(ACCOUNT_TYPES).keys():
            raise ValueError('default_account_type must be one of ACCOUNT_TYPES')
        return self.default_account_type

    def get_user_key(self):
        return f'{self.default_account_type}'

    @staticmethod
    def construct_user_key(phone_number):
        return NotImplementedError()

    @property
    def try_athlete(self):
        from account.models import Athlete
        if isinstance(self, Athlete):
            return self
        try:
            return self.athlete
        except:
            return None

    @property
    def try_gym_owner(self):
        from account.models import GymOwner
        if isinstance(self, GymOwner):
            return self
        try:
            return self.gymowner
        except:
            return None

    @property
    def concrete_instance(self):
        return self.try_athlete or self.try_gym_owner

    def before_create(self):
        from financial.models import Wallet
        from crm.models import CRMAccount
        self.wallet = Wallet.objects.create()
        self.crm_account = CRMAccount.objects.create()
        if not self.account_type:
            self.account_type = self.get_default_account_type()
        # Todo: Fix Username Problem
        self.user = get_user_model().objects.create(
            username=self.get_user_key()
        )

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب‌های کاربری'

    jwt_claim_keys = [
        ('id', 'account_id'),
        'wallet_id',
        'crm_account_id',
        'account_type',
    ]
