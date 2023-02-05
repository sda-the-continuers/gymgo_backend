import operator
from functools import lru_cache

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from rest_framework.fields import get_attribute

from discount.utils import RestrictionData, DiscountApplierComponent
from utility.models import HistoricalBaseModel


class DiscountRestriction(HistoricalBaseModel):
    field = None
    value = None
    operator_function_name = None

    discount = models.ForeignKey(
        to='discount.Discount',
        on_delete=models.CASCADE,
        verbose_name='تخفیف',
    )

    @property
    def operator_function(self):
        return getattr(operator, self.operator_function_name)

    def apply_operator(self, other_value):
        return self.operator_function(other_value, self.value)

    @cached_property
    def source_attrs(self):
        return self.field.split('.')

    def translate_value(self, value) -> str:
        return str(value)

    def _raise_validation_error(self, value_from_campaign):
        raise ValidationError(
            '"{field}" که "{given_value}" است باید {operator} "{value}" باشد.'.format(
                field=self.get_field_display(),
                given_value=self.translate_value(value_from_campaign),
                operator=self.get_operator_function_name_display(),
                value=self.translate_value(self.value),
            )
        )

    def get_real_value(self, component):
        return get_attribute(RestrictionData.from_discount_applier_component(self, component), self.source_attrs)

    def can_apply_to(self, component: DiscountApplierComponent, raise_exception=False):
        real_value = self.get_real_value(component)
        if self.apply_operator(real_value):
            return True
        elif not raise_exception:
            return False
        else:
            self._raise_validation_error(value_from_campaign=real_value)

    @lru_cache()
    def get_info(self):
        from discount.utils.discount_restriction_info import DiscountRestrictionInfo
        return DiscountRestrictionInfo(self)

    def __str__(self):
        return 'محدودیت تخفیف {}: {}'.format(
            self.id,
            self.get_info()
        )

    @property
    def try_integer_discount_restriction(self):
        from discount.models import IntegerDiscountRestriction
        if isinstance(self, IntegerDiscountRestriction):
            return self
        try:
            return self.integerdiscountrestriction
        except:
            return None

    @property
    def try_date_time_discount_restriction(self):
        from discount.models import DateTimeDiscountRestriction
        if isinstance(self, DateTimeDiscountRestriction):
            return self
        try:
            return self.datetimediscountrestriction
        except:
            return None

    @property
    def try_text_discount_restriction(self):
        from discount.models import TextDiscountRestriction
        if isinstance(self, TextDiscountRestriction):
            return self
        try:
            return self.textdiscountrestriction
        except:
            return None

    @property
    def try_boolean_discount_restriction(self):
        from discount.models import BooleanDiscountRestriction
        if isinstance(self, BooleanDiscountRestriction):
            return self
        try:
            return self.booleandiscountrestriction
        except:
            return None

    @property
    def concrete_instance(self):
        return (
                self.try_integer_discount_restriction or
                self.try_date_time_discount_restriction or
                self.try_text_discount_restriction or
                self.try_boolean_discount_restriction
        )

    class Meta:
        abstract = True
