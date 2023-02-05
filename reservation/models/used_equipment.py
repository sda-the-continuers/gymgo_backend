from django.db import models

from utility.models import HistoricalBaseModel


class UsedEquipment(HistoricalBaseModel):
    gym_equipment = models.ForeignKey(
        to='gym.GymUsageEquipment',
        on_delete=models.CASCADE,
        related_name='used_equipments',
        verbose_name='تجهیز مربوطه',
    )

    reserve = models.ForeignKey(
        to='reservation.Reserve',
        on_delete=models.CASCADE,
        related_name='used_equipments',
        verbose_name='رزرو مربوطه',
    )

    class Meta:
        verbose_name = 'تجهیز استفاده شده'
        verbose_name_plural = 'تجهیزات استفاده شده'
