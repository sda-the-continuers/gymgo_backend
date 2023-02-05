import typing

from django.db import models

from utility.math import round_to_thousand
from utility.models import HistoricalBaseModel, PercentageField


class DiscountPricingType(HistoricalBaseModel):

    @property
    def try_fixed_discount_pricing_type(self):
        if isinstance(self, FixedDiscountPricingType):
            return self
        try:
            return self.fixeddiscountpricingtype
        except:
            return None

    @property
    def try_percentage_discount_pricing_type(self):
        if isinstance(self, PercentageDiscountPricingType):
            return self
        try:
            return self.percentagediscountpricingtype
        except:
            return None

    @property
    def concrete_instance(self):
        return self.try_fixed_discount_pricing_type or self.try_percentage_discount_pricing_type

    def get_discount_amount(self, price: int):
        raise NotImplementedError

    class Meta:
        verbose_name = 'نوع قیمت‌گذاری تخفیف'
        verbose_name_plural = 'انواع قیمت‌گذاری تخفیف'


class FixedDiscountPricingType(DiscountPricingType):

    def get_discount_amount(self, price: int):
        return min(price, self.discount_amount)

    discount_amount = models.PositiveIntegerField(
        verbose_name='مقدار تخفیف',
    )

    class Meta:
        verbose_name = 'نوع قیمت‌گذاری ثابت تخفیف'
        verbose_name_plural = 'انواع قیمت‌گذاری ثابت تخفیف'


class PercentageDiscountPricingType(DiscountPricingType):

    def get_discount_amount(self, price: int):
        discount_amount = min(price, round_to_thousand(price * self.discount_percentage_amount / 100))
        if self.maximum_discount_amount is not None:
            discount_amount = min(discount_amount, self.maximum_discount_amount)
        return int(discount_amount)

    discount_percentage_amount = PercentageField(
        verbose_name='درصد تخفیف',
    )

    maximum_discount_amount = models.PositiveIntegerField(
        verbose_name='حداکثر مقدار تخفیف',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'نوع قیمت‌گذاری درصدی تخفیف'
        verbose_name_plural = 'انواع قیمت‌گذاری درصدی تخفیف'
