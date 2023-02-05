from django.db import models

from utility.models import CreateHistoryModel


class SportTypeIcon(CreateHistoryModel):

    sport_type = models.OneToOneField(
        to='gym.SportType',
        on_delete=models.CASCADE,
        related_name='icon',
        verbose_name='نوع ورزش مربوطه',
    )

    file = models.FileField(
        upload_to='sport_icon',
        verbose_name='فایل',
    )

    class Meta:
        verbose_name = 'آیکون ورزشی'
        verbose_name_plural = 'آیکون‌های ورزشی'
