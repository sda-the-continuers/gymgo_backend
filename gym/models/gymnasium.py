from django.db import models

from gym.models import GymContentMediaMixin
from utility.models import HistoricalBaseModel, PositiveFloatField, EnumBaseModel


class GymnasiumAttribute(EnumBaseModel): pass


class Gymnasium(GymContentMediaMixin, HistoricalBaseModel):
    gym_complex = models.ForeignKey(
        to='gym.GymComplex',
        on_delete=models.CASCADE,
        related_name='gymnasiums',
        verbose_name='مجموعه مربوطه',
    )

    type = models.ForeignKey(
        to='gym.GymnasiumType',
        related_name='gymnasiums',
        verbose_name='نوع ورزشگاه',
        on_delete=models.PROTECT,
    )

    description = models.TextField(
        verbose_name='توضیحات',
        null=True,
        blank=True
    )

    price = models.PositiveIntegerField(
        verbose_name='مبلغ',
        null=True,
        blank=True,
    )

    gym_owner_price = models.PositiveIntegerField(
        verbose_name='مبلغ پرداختی به صاحب ورزشگاه',
        null=True,
        blank=True,
    )

    rules = models.TextField(
        verbose_name='قوانین',
        null=True,
        blank=True,
    )

    length = PositiveFloatField(
        verbose_name='طول',
        help_text='به متر',
    )

    width = PositiveFloatField(
        verbose_name='عرض',
        help_text='به متر',
    )

    attributes = models.ManyToManyField(
        to=GymnasiumAttribute,
        related_name='gymnasiums',
        verbose_name='امکانات ورزشگاه',
        blank=True,
    )

    def get_final_rules(self):
        return self.rules or self.gym_complex.rules

    @property
    def comments(self):
        from reservation.models import Comment
        return Comment.get_comments_for_gym(self)

    class Meta:
        verbose_name = 'ورزشگاه'
        verbose_name_plural = 'ورزشگاه‌ها'
