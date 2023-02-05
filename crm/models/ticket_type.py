from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utility.models import BaseModel, EnumBaseModel


class TicketType(EnumBaseModel, BaseModel):
    priority = models.IntegerField(
        verbose_name='اولویت',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        verbose_name = 'نوع تیکت'
        verbose_name_plural = 'نوع تیکت‌ها'
