from django.db import models

from utility.models import BaseModel, EnumBaseModel


class GymnasiumType(EnumBaseModel, BaseModel):
    sport_types = models.ManyToManyField(
        to='gym.SportType',
        related_name='gymnasium_types',
        verbose_name='انواع ورزش‌های مربوطه',
        blank=True,
    )

    class Meta:
        verbose_name = 'نوع ورزشگاه'
        verbose_name_plural = 'انواع ورزشگاه'
