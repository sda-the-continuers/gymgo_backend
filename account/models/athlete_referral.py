from django.db import models

from utility.models import HistoricalBaseModel


class AthleteReferral(HistoricalBaseModel):

    referred_athlete = models.OneToOneField(
        to='account.athlete',
        related_name='referral',
        on_delete=models.CASCADE,
        verbose_name='ورزشکار معرفی شده'
    )

    referrer_athlete = models.ForeignKey(
        to='account.athlete',
        related_name='referrals',
        on_delete=models.CASCADE,
        verbose_name='ورزشکار معرف'
    )

    class Meta:
        verbose_name = 'معرفی ورزشکار'
        verbose_name_plural = 'معرفی‌های ورزشکار'