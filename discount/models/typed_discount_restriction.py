from django.core.exceptions import ValidationError
from django.db import models

from utility.text_processing import jalali_strfdatetime
from .discount_restriction import DiscountRestriction
from ..enums import INTEGER_RESTRICTION_FIELD_CHOICES, TEXT_RESTRICTION_FIELD_CHOICES, \
    BOOLEAN_RESTRICTION_FIELD_CHOICES, DATETIME_RESTRICTION_FIELD_CHOICES, COMPARABLE_OPERATORS, EQUALITY_OPERATORS, \
    TEXT_OPERATORS


class IntegerDiscountRestriction(DiscountRestriction):
    value = models.IntegerField(verbose_name='مقدار')
    field = models.CharField(
        max_length=1024,
        choices=INTEGER_RESTRICTION_FIELD_CHOICES,
        verbose_name='فیلد مورد نظر',
    )
    operator_function_name = models.CharField(
        max_length=16,
        choices=(*EQUALITY_OPERATORS, *COMPARABLE_OPERATORS),
        verbose_name='نام تابع عملگر',
    )

    class Meta:
        verbose_name = 'محدودیت تخفیف عددی'
        verbose_name_plural = 'محدودیت‌های تخفیف عددی'


class DateTimeDiscountRestriction(DiscountRestriction):
    value = models.DateTimeField(verbose_name='مقدار')
    field = models.CharField(
        max_length=1024,
        choices=DATETIME_RESTRICTION_FIELD_CHOICES,
        verbose_name='فیلد مورد نظر',
    )
    operator_function_name = models.CharField(
        max_length=16,
        choices=COMPARABLE_OPERATORS,
        verbose_name='نام تابع عملگر',
    )

    def translate_value(self, value) -> str:
        return jalali_strfdatetime(value)

    class Meta:
        verbose_name = 'محدودیت تخفیف زمانی'
        verbose_name_plural = 'محدودیت‌های تخفیف زمانی'


class TextDiscountRestriction(DiscountRestriction):
    value = models.TextField(verbose_name='مقدار')
    field = models.CharField(
        max_length=1024,
        choices=TEXT_RESTRICTION_FIELD_CHOICES,
        verbose_name='فیلد مورد نظر',
    )
    operator_function_name = models.CharField(
        max_length=16,
        choices=(*EQUALITY_OPERATORS, *TEXT_OPERATORS),
        verbose_name='نام تابع عملگر',
    )

    class Meta:
        verbose_name = 'محدودیت تخفیف متنی'
        verbose_name_plural = 'محدودیت‌های تخفیف متنی'


class BooleanDiscountRestriction(DiscountRestriction):
    value = models.BooleanField(verbose_name='مقدار')
    field = models.CharField(
        max_length=1024,
        choices=BOOLEAN_RESTRICTION_FIELD_CHOICES,
        verbose_name='فیلد مورد نظر',
    )
    operator_function_name = models.CharField(
        max_length=16,
        choices=EQUALITY_OPERATORS,
        verbose_name='نام تابع عملگر',
    )

    def translate_value(self, value) -> str:
        return 'است' if value else 'نیست'

    def _raise_validation_error(self, value_from_campaign):
        raise ValidationError(
            'این کد تخفیف برای "{field}" {value}.'.format(
                field=self.get_field_display(),
                value=self.translate_value(self.value),
            )
        )

    def translate_value(self, value):
        return 'بله' if value else 'خیر'

    class Meta:
        verbose_name = 'محدودیت تخفیف منطقی'
        verbose_name_plural = 'محدودیت‌های تخفیف منطقی'
