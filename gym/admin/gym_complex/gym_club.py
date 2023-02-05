from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from discount.admin import DiscountBaseAdmin
from gym.models import Club, ClubContact, ClubDiscount
from utility.admin.utility_link_admin import UtilityLinkAdmin


class ClubContactInline(UtilityLinkAdmin, NestedStackedInline):
    model = ClubContact
    extra = 1
    fields = [
        'full_name',
        'phone_number',
        'athlete',
        'get_athlete',
    ]

    readonly_fields = ['get_athlete']

    def get_athlete(self, instance: ClubContact):
        return self.link_display_style_raw(instance.athlete)

    get_athlete.short_description = ClubContact.get_field('athlete').verbose_name


class ClubDiscountInline(DiscountBaseAdmin, UtilityLinkAdmin, NestedStackedInline):
    model = ClubDiscount
    extra = 1

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets.append(
            ('اطلاعات مربوط به باشگاه مخاطبین', {
                'fields': (
                    'contacts',
                ),
            }),
        )
        return fieldsets


# TODO: ClubSMS admin


@admin.register(Club)
class GymClubAdmin(UtilityLinkAdmin, NestedModelAdmin):
    inlines = [
        ClubContactInline,
        ClubDiscountInline,
    ]
