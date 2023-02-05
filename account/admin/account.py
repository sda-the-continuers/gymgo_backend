from django.contrib.admin import ModelAdmin
from django.urls import reverse

from account.models import Account
from utility.admin.utility_link_admin import UtilityLinkAdmin


class AccountAdmin(UtilityLinkAdmin, ModelAdmin):

    fieldsets = [
        ('اطلاعات Account', {
            'fields': (
                'full_name',
                'get_user',
                'get_wallet',
                'get_crm_account',
                'account_type',
            ),
        }),
    ]

    readonly_fields = [
        'get_user',
        'get_wallet',
        'get_crm_account',
        'account_type',
    ]

    def get_user(self, instance: Account):
        return self.link_display_style_raw(
            instance.user,
            admin_url=reverse('admin:{}_{}_change'.format('auth', 'user'), args=[instance.user.id]),
            verbose_name=Account.get_field('user').verbose_name
        )

    get_user.short_description = Account.get_field('user').verbose_name

    def get_wallet(self, instance: Account):
        return self.link_display_style_raw(instance.wallet)

    get_wallet.short_description = Account.get_field('wallet').verbose_name

    def get_crm_account(self, instance: Account):
        return self.link_display_style_raw(instance.crm_account)

    get_crm_account.short_description = Account.get_field('crm_account').verbose_name


