from typing import List

from django.db import models

from sms.models import GymtimeSimpleSMS
from utility.models import BaseModel, filter_active_objects


class GymtimeSMS(GymtimeSimpleSMS):

    def get_receptors(self) -> List[str]:
        return list(filter_active_objects(self.receptors_set).values_list('phone_number'))

    class Meta:
        verbose_name = 'پیامک جیم‌تایم'
        verbose_name_plural = 'پیامک‌های جیم‌تایم'


class GymtimeSMSReceptor(BaseModel):

    phone_number = models.CharField(
        max_length=32,
        verbose_name='شماره همراه',
    )

    sms = models.ForeignKey(
        to=GymtimeSMS,
        on_delete=models.CASCADE,
        related_name='receptors_set',
        verbose_name='پیامک مربوطه',
    )

    class Meta:
        verbose_name = 'گیرنده پیامک جیم‌تایم'
        verbose_name_plural = 'گیرندگان پیامک جیم‌تایم'
