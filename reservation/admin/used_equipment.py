from django.contrib import admin

from reservation.models import UsedEquipment


@admin.register(UsedEquipment)
class UsedEquipmentAdmin(admin.ModelAdmin):
    pass
