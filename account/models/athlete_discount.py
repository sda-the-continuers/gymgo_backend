from django.db import models
from django.db.models import QuerySet

from discount.models import AthleteBasedDiscount


class AthleteDiscount(AthleteBasedDiscount):
    athletes = models.ManyToManyField(
        to='account.athlete',
        related_name='discounts',
        verbose_name='تبلیغ‌کننده',
    )

    @property
    def athletes_that_can_apply(self) -> QuerySet:
        return self.athletes.all()

    class Meta:
        verbose_name = 'تخفیف اختصاصی ورزشکار'
        verbose_name_plural = 'تخفیف‌های اختصاصی ورزشکار'
