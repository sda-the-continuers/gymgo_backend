from typing import Union, TYPE_CHECKING

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, ModelSerializer

from discount.enums import DATETIME_RESTRICTION_FIELD_NOW, OPERATOR_LT, INTEGER_RESTRICTION_FIELD_REPEATS
from discount.models import Discount, DateTimeDiscountRestriction, IntegerDiscountRestriction
from utility.python import safe_pop, safe_multipop

if TYPE_CHECKING:
    from discount.serializer import PercentageDiscountPricingTypeDeserializer, FixedDiscountPricingTypeDeserializer


class DiscountPricingTypeGeneralDeserializer(Serializer):
    discount_percentage_amount = serializers.FloatField(allow_null=True, required=False)
    maximum_discount_amount = serializers.IntegerField(allow_null=True, required=False)
    discount_amount = serializers.IntegerField(allow_null=True, required=False)

    @staticmethod
    def get_pricing_type_serializer(validated_data, context) -> Union[
        'PercentageDiscountPricingTypeDeserializer', 'FixedDiscountPricingTypeDeserializer'
    ]:
        if (validated_data.get('discount_percentage_amount') is not None) == (
                validated_data.get('discount_amount') is not None):
            raise ValidationError({
                'discount_percentage_amount': ['لطفا یک نوع تخفیف را انتخاب کنید. انتخاب‌های موجود: درصدی، مقداری!']
            })

        if validated_data.get('discount_percentage_amount') is not None:
            from discount.serializer import PercentageDiscountPricingTypeDeserializer
            safe_pop(validated_data, 'discount_amount')
            serializer_class = PercentageDiscountPricingTypeDeserializer
        else:
            from discount.serializer import FixedDiscountPricingTypeDeserializer
            safe_multipop(validated_data, 'discount_percentage_amount', 'maximum_discount_amount')
            serializer_class = FixedDiscountPricingTypeDeserializer
        return serializer_class(data=validated_data, context=context)

    class Meta:
        fields = [
            'discount_percentage_amount',
            'maximum_discount_amount',
            'discount_amount',
        ]


class DiscountDeserializer(ModelSerializer):
    general_pricing_type = DiscountPricingTypeGeneralDeserializer()
    until = serializers.DateTimeField(allow_null=True, required=False)
    repeats = serializers.IntegerField(allow_null=True, required=False)

    def validate_until(self, value):
        if value is None or value >= timezone.now() + timezone.timedelta(hours=1):
            return value
        raise ValidationError({'until': ['فرصت تخفیف باید حداقل یک ساعت باشد!']})

    def validate_repeats(self, value):
        if value is None or value > 0:
            return value
        raise ValidationError({'repeats': ['تعداد تکرار باید یک عدد مثبت باشد!']})

    def try_creating_until_restriction(self, discount: Discount, until):
        if until is None:
            return None
        return DateTimeDiscountRestriction.objects.create(
            value=until,
            field=DATETIME_RESTRICTION_FIELD_NOW,
            operator_function_name=OPERATOR_LT,
            discount=discount,
        )

    def try_creating_repeats_restriction(self, discount: Discount, repeats):
        if repeats is None:
            return None
        return IntegerDiscountRestriction.objects.create(
            value=repeats,
            field=INTEGER_RESTRICTION_FIELD_REPEATS,
            operator_function_name=OPERATOR_LT,
            discount=discount,
        )

    def create(self, validated_data):
        with transaction.atomic():
            pricing_type_serializer = DiscountPricingTypeGeneralDeserializer.get_pricing_type_serializer(
                validated_data.pop('general_pricing_type'), self.context
            )
            pricing_type_serializer.is_valid(raise_exception=True)
            validated_data['pricing_type'] = pricing_type_serializer.save()
            repeats, until = safe_multipop(validated_data, 'repeats', 'until')
            discount = super().create(validated_data)
            self.try_creating_until_restriction(discount, until)
            self.try_creating_repeats_restriction(discount, repeats)
            return discount

    class Meta:
        model = Discount
        fields = [
            'code',
            'repeats',
            'until',
            'general_pricing_type',
        ]
