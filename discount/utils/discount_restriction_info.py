import typing
from discount.enums.discount_restriction import *

from discount.models import IntegerDiscountRestriction, DateTimeDiscountRestriction

if typing.TYPE_CHECKING:
    from discount.models import DiscountRestriction


class DiscountRestrictionInfoBase(object):
    def __getattr__(self, item):
        return getattr(self.round_rubbing_task, item)

    inherited_methods = [
        'get_operator_function_name_display',
        'translate_value',
    ]

    def __init__(self, discount_restriction: "DiscountRestriction"):
        for method in self.inherited_methods:
            setattr(self, method, getattr(discount_restriction, method))

    def __new__(cls, discount_restriction: "DiscountRestriction", *args, **kwargs):
        discount_restriction = discount_restriction.concrete_instance
        if isinstance(discount_restriction, IntegerDiscountRestriction):
            return super().__new__(IntegerDiscountRestrictionInfo)
        if isinstance(discount_restriction, DateTimeDiscountRestriction):
            return super().__new__(DateTimeDiscountRestrictionInfo)
        return super().__new__(DiscountRestrictionInfo)


class DiscountRestrictionInfo(DiscountRestrictionInfoBase):

    def get_info_template(self) -> str:
        return '{field} {operator} {value}'

    def get_field_info(self) -> str:
        return self.get_field_info()

    def get_value_info(self) -> str:
        return self.translate_value(self.value)

    def get_operator_info(self) -> str:
        return self.get_operator_function_name_display()

    def get_info(self) -> str:
        return self.get_info_template().format(
            field=self.get_field_info(),
            operator=self.get_operator_info(),
            value=self.get_value_info(),
        )


class IntegerDiscountRestrictionInfo(DiscountRestrictionInfo):
    INTEGER_RESTRICTION_FIELD_INFO = {
        INTEGER_RESTRICTION_FIELD_GYM_COMPLEX_ID: 'مجموعه ورزشی',
        INTEGER_RESTRICTION_FIELD_GYMNASIUM_ID: 'سالن',
    }

    def get_field_info(self):
        return self.INTEGER_RESTRICTION_FIELD_INFO.get(
            self.field, dict(INTEGER_RESTRICTION_FIELD_CHOICES)[self.field]
        )

    def get_value_info(self):
        from gym.models import GymComplex, Gymnasium
        if self.field == INTEGER_RESTRICTION_FIELD_GYM_COMPLEX_ID:
            return 'با کد {}'.format(GymComplex.objects.get(id=self.value).code)
        if self.field == INTEGER_RESTRICTION_FIELD_GYMNASIUM_ID:
            gymnasuim = Gymnasium.objects.get(id=self.value)
            return '{} با کد {}'.format(gymnasuim.type.title_fa, gymnasuim.gym_complex.code)
        return self.value

    def get_info_template(self) -> str:
        if self.field in self.INTEGER_RESTRICTION_FIELD_INFO:
            return '{field} {value}'
        else:
            return '{field} {operator} {value}'


class DateTimeDiscountRestrictionInfo(DiscountRestrictionInfo):
    COMPARABLE_OPERATORS_FOR_DATETIME_INFO = {
        OPERATOR_LT: 'تا',
        OPERATOR_LE: 'تا',
        OPERATOR_GT: 'از',
        OPERATOR_GE: 'از'
    }

    def get_operator_info(self) -> str:
        return self.COMPARABLE_OPERATORS_FOR_DATETIME_INFO[self.operator]
