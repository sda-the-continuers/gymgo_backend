from django.conf import settings
from django.db import models

from gym.models import GymContentMediaMixin
from utility.models import HistoricalBaseModel, BaseLocationModel
from utility.random import generate_random_number


def generate_gym_complex_code():
    while GymComplex.objects.all().filter(
            code=(code := generate_random_number(settings.GYM_COMPLEX_CODE_LENGTH))
    ).exists(): pass
    return code


class GymComplex(GymContentMediaMixin, BaseLocationModel, HistoricalBaseModel):
    code = models.CharField(
        max_length=10,
        verbose_name='کد مجموعه ورزشی',
        unique=True,
        db_index=True,
        default=generate_gym_complex_code,
    )

    phone_number = models.CharField(
        max_length=32,
        verbose_name='شماره تماس مجموعه',
    )

    name = models.CharField(
        max_length=128,
        verbose_name='نام مجموعه',
    )

    owner = models.ForeignKey(
        to='account.GymOwner',
        on_delete=models.CASCADE,
        related_name='gym_complexes',
        verbose_name='صاحب ورزشگاه'
    )

    address = models.TextField(
        verbose_name='آدرس متنی',
    )

    description = models.TextField(
        verbose_name='توضیحات',
        null=True,
        blank=True,
    )

    rules = models.TextField(
        verbose_name='قوانین',
        null=True,
        blank=True,
    )

    instagram_username = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='آیدی اینستاگرام مجموعه ورزشی',
    )

    club = models.OneToOneField(
        to='gym.Club',
        related_name='gym_complex',
        verbose_name='باشگاه مخاطبین',
        on_delete=models.PROTECT,
    )

    def before_create(self):
        super().before_create()
        from gym.models import Club
        self.club = Club.objects.create()

    class Meta:
        verbose_name = 'مجموعه ورزشی'
        verbose_name_plural = 'مجموعه‌های ورزشی'
