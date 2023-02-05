from django.contrib.admin import ModelAdmin

from account.models import AthleteReferral
from django.contrib import admin


@admin.register(AthleteReferral)
class AthleteReferralAdmin(ModelAdmin):
    list_display = [
        'id',
        'get_referrer',
        'get_referred'
    ]

    readonly_fields = [
        'referred_athlete',
        'referrer_athlete',
    ]

    @admin.display(description='معرفی کننده')
    def get_referrer(self, obj):
        return self.link_display_style_detailed(obj.referrer_athlete, 'phone_number')

    @admin.display(description='معرفی شده')
    def get_referred(self, obj):
        return self.link_display_style_detailed(obj.referred_athlete, 'phone_number')
