from typing import List

from django.db import models

from gym.models.club import ClubRelatedMixin
from sms.models import GymtimeSimpleSMS


class ClubSMS(ClubRelatedMixin, GymtimeSimpleSMS):

    def get_receptors(self) -> List[str]:
        return list(self.contacts.values_list('phone_number', flat=True))

    class Meta:
        verbose_name = 'پیامک کلاب'
        verbose_name_plural = 'پیامک‌های کلاب'


class ClubSMSForDiscount(ClubSMS):
    # make it foreign key maybe in future one discount is notified through multiple sms messages
    discount = models.ForeignKey(
        to='gym.ClubDiscount',
        related_name='club_sms',
        verbose_name='تخفیف مربوطه',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'پیامک تخفیف کلاب'
        verbose_name_plural = 'پیامک‌های تخفیف کلاب'
