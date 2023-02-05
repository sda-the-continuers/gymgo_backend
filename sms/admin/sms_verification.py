from django.contrib import admin

from sms.models import SMSVerification
from utility.admin import BaseAdmin


@admin.register(SMSVerification)
class SMSVerificationAdmin(BaseAdmin):

    list_display = [
        'id',
        'phone_number',
        'usage_type',
        'account_type',
        'is_used'
    ]

    @admin.display(description='صاحب')
    def get_owner(self, obj):
        return self.link_display_style_raw(obj.owner)
