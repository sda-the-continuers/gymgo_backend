from django.contrib import admin

from financial.models import Transaction
from utility.admin import BaseAdmin


@admin.register(Transaction)
class TransactionAdmin(BaseAdmin):

    list_display = [
        'id',
        'get_wallet',
        'amount',
        'description'
    ]

    @admin.display(description='کیف پول')
    def get_wallet(self, obj):
        return self.link_display_style_raw(obj.wallet)
