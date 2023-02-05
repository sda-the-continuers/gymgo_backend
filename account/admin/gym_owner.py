from django.contrib import admin

from account.admin import AccountAdmin
from account.models import GymOwner


@admin.register(GymOwner)
class GymOwnerAdmin(AccountAdmin):
    list_display = [
        'id',
        'phone_number',
        'full_name',
        'shaba',
    ]

    fieldsets = [
        *AccountAdmin.fieldsets,
        (
            'اطلاعات صاحب سالن', {
                'fields': (
                    'phone_number',
                    'shaba',
                )
            }
        )
    ]
