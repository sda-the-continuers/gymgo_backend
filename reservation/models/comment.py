from typing import Union, TYPE_CHECKING

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utility.models import BaseModel

if TYPE_CHECKING:
    from gym.models import GymComplex, Gymnasium, GymUsage


class Comment(BaseModel):
    score = models.PositiveIntegerField(
        verbose_name='امتیاز',
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    reserve = models.OneToOneField(
        to='reservation.Reserve',
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='رزرو مربوطه',
    )

    comment_text = models.TextField(
        verbose_name='متن نظر',
        null=True,
        blank=True,
    )

    @classmethod
    def get_comments_for_gym(cls, gym: Union['GymComplex', 'Gymnasium', 'GymUsage']):
        from gym.models import GymComplex, Gymnasium, GymUsage
        return cls.objects.filter(
            **{
                {
                    GymComplex: 'reserve__gym_usage__gymnasium__gym_complex_id',
                    Gymnasium: 'reserve__gym_usage__gymnasium_id',
                    GymUsage: 'reserve__gym_usage_id',
                }[type(gym)]: gym.id
            }
        )

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
