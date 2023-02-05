from rest_framework.serializers import ModelSerializer

from discount.models import FixedDiscountPricingType, PercentageDiscountPricingType


class FixedDiscountPricingTypeDeserializer(ModelSerializer):
    class Meta:
        model = FixedDiscountPricingType
        fields = [
            'discount_amount',
        ]


class PercentageDiscountPricingTypeDeserializer(ModelSerializer):

    class Meta:
        model = PercentageDiscountPricingType
        fields = [
            'discount_percentage_amount',
            'maximum_discount_amount',
        ]
