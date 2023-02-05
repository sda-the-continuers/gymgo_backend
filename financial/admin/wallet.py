from django.contrib import admin

from financial.models import Wallet
from utility.admin import BaseAdmin


@admin.register(Wallet)
class WalletAdmin(BaseAdmin):

    list_display = [
        'id',
        'total_amount',
        'get_account'
    ]

    @admin.display(description='اکانت مربوطه')
    def get_account(self, obj):
        return self.link_display_style_raw(obj.account.concrete_instance)
