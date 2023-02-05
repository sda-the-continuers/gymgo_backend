from django.conf import settings
from django.db import models
from jalali_date import date2jalali
from simple_history.utils import bulk_update_with_history

from account.enums import ATHLETE_GENDERS, ACCOUNT_TYPE_ATHLETE
from account.models import Account, PhoneNumberMixin
from utility.random import generate_random_alphabetic_code


def generate_referral_code():
    while Athlete.objects.all().filter(
            referral_code=(code := generate_random_alphabetic_code(settings.REFERRAL_CODE_LENGTH))
    ).exists(): pass
    return code


class Athlete(PhoneNumberMixin, Account):
    default_account_type = ACCOUNT_TYPE_ATHLETE

    gender = models.CharField(
        max_length=64,
        choices=ATHLETE_GENDERS,
        verbose_name='جنسیت',
        null=True,
        blank=True,
    )

    birth_date = models.DateField(
        verbose_name='تاریخ تولد',
        null=True,
        blank=True,
    )

    favorite_sports = models.ManyToManyField(
        to='gym.SportType',
        related_name='athletes',
        verbose_name='ورزش‌های مورد علاقه',
        blank=True,
    )

    referral_code = models.CharField(
        max_length=16,
        default=generate_referral_code,
        verbose_name='کد معرفی'
    )

    @property
    def jalali_birth_date(self):
        return date2jalali(self.birth_date)

    @staticmethod
    def construct_user_key(phone_number):
        return f'{Athlete.default_account_type}-{phone_number}'

    def before_create(self):
        super().before_create()
        from gym.models.club.club_contact import ClubContact

        def set_athlete_on_club_concat(club_contact: ClubContact):
            club_contact.athlete = self
            return club_contact

        bulk_update_with_history(
            [
                set_athlete_on_club_concat(club_contact)
                for club_contact in ClubContact.objects.filter(phone_number=self.phone_number)
            ],
            model=ClubContact,
            fields=['athlete'],
        )

    class Meta:
        verbose_name = 'ورزشکار'
        verbose_name_plural = 'ورزشکاران'
