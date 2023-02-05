from django.db import models

from gym.enums import GYM_USAGE_EQUIPMENT_TYPES
from utility.models import BaseModel


class GymUsageEquipment(BaseModel):
    gym_usage = models.ForeignKey(
        to='gym.GymUsage',
        on_delete=models.CASCADE,
        related_name='equipments',
        verbose_name='کاربری ورزشگاه مربوطه',
    )

    type = models.CharField(
        choices=GYM_USAGE_EQUIPMENT_TYPES,
        max_length=256,
        verbose_name='نوع تجهیز کاربری ورزشگاه',
    )

    price = models.PositiveIntegerField(
        verbose_name='مبلغ امکانات'
    )

    class Meta:
        verbose_name = 'تجهیز کاربری ورزشگاه'
        verbose_name_plural = 'تجهیزات کاربری ورزشگاه'
