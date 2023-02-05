from nested_admin.nested import NestedStackedInline

from gym.models import GymUsage, GymUsageEquipment


class GymUsageEquipmentInline(NestedStackedInline):
    model = GymUsageEquipment
    extra = 1
    fields = [
        'type',
        'price',
    ]


class GymUsageInline(NestedStackedInline):
    model = GymUsage
    extra = 1

    fields = [
        'type',
    ]

    inlines = [
        GymUsageEquipmentInline,
    ]
