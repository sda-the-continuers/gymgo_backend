from django.db import models

from utility.models import HistoricalBaseModel


class Wallet(HistoricalBaseModel):

    total_amount = models.IntegerField(
        verbose_name='موجودی',
        default=0,
    )

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول‌ها'
