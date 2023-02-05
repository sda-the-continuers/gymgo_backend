from django.contrib import admin
from django.contrib.admin import ModelAdmin
from nested_admin.nested import NestedTabularInline

from discount.models import Discount, FixedDiscountPricingType, PercentageDiscountPricingType, DiscountRestriction, \
    IntegerDiscountRestriction, DateTimeDiscountRestriction, TextDiscountRestriction, BooleanDiscountRestriction


class DiscountRestrictionInline(NestedTabularInline):
    model = DiscountRestriction
    extra = 1
    fields = [
        'field',
        'value',
        'operator_function_name',
        'get_info',
    ]

    readonly_fields = [
        'get_info',
    ]

    def get_info(self, instance: DiscountRestriction):
        if not instance.id:
            return '---'
        return instance.get_info()

    get_info.short_description = 'توضیحات'


class IntegerDiscountRestrictionInline(DiscountRestrictionInline):
    model = IntegerDiscountRestriction


class DateTimeDiscountRestrictionInline(DiscountRestrictionInline):
    model = DateTimeDiscountRestriction


class TextDiscountRestrictionInline(DiscountRestrictionInline):
    model = TextDiscountRestriction


class BooleanDiscountRestrictionInline(DiscountRestrictionInline):
    model = BooleanDiscountRestriction


class DiscountBaseAdmin:
    list_display_links = [
        'get_str',
        'code',
    ]

    list_display = [
        'get_str',
        'code',
        'get_discount_amount',
        'get_discount_percentage_amount',
        'get_maximum_discount_amount',
    ]

    fieldsets = [
        (None, {
            'fields': (
                'code',
                'pricing_type',
                'get_discount_amount',
                'get_discount_percentage_amount',
                'get_maximum_discount_amount',
            ),
        }),
    ]

    readonly_fields = [
        'get_discount_amount',
        'get_discount_percentage_amount',
        'get_maximum_discount_amount',
    ]

    inlines = [
        IntegerDiscountRestrictionInline,
        DateTimeDiscountRestrictionInline,
        TextDiscountRestrictionInline,
        BooleanDiscountRestrictionInline,
    ]

    def get_str(self, instance):
        return str(instance)

    get_str.short_description = 'توضیحات'
    get_str.admin_order_field = 'id'

    def get_discount_amount(self, instance: Discount):
        if instance.pricing_type:
            concrete_pricing_type = instance.pricing_type.concrete_instance
            if isinstance(concrete_pricing_type, FixedDiscountPricingType):
                return concrete_pricing_type.discount_amount
        return '---'

    get_discount_amount.short_description = 'میزان تخفیف'

    def get_discount_percentage_amount(self, instance: Discount):
        if instance.pricing_type:
            concrete_pricing_type = instance.pricing_type.concrete_instance
            if isinstance(concrete_pricing_type, PercentageDiscountPricingType):
                return concrete_pricing_type.discount_percentage_amount
        return '---'

    get_discount_percentage_amount.short_description = 'درصد تخفیف'

    def get_maximum_discount_amount(self, instance: Discount):
        if instance.pricing_type:
            concrete_pricing_type = instance.pricing_type.concrete_instance
            if isinstance(concrete_pricing_type, PercentageDiscountPricingType):
                return concrete_pricing_type.maximum_discount_amount
        return '---'

    get_maximum_discount_amount.short_description = 'حداکثر تخفیف'


@admin.register(Discount)
class DiscountAdmin(DiscountBaseAdmin, ModelAdmin):
    pass
