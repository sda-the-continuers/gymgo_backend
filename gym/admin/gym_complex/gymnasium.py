from jalali_date.admin import ModelAdminJalaliMixin
from nested_admin.nested import NestedStackedInline

from gym.admin.gym_complex import GymUsageInline
from gym.models import Gymnasium, ScheduledSession
from utility.admin.utility_link_admin import UtilityLinkAdmin


class ScheduledSessionInline(ModelAdminJalaliMixin, NestedStackedInline):
    model = ScheduledSession
    extra = 1
    fields = [
        'start_datetime',
        'end_datetime',
        'state',
        'price',
        'gym_owner_price',
    ]


class GymnasiumInline(UtilityLinkAdmin, NestedStackedInline):

    model = Gymnasium
    extra = 1

    fields = [
        'type',
        'description',
        'price',
        'gym_owner_price',
        'rules',
        'attributes',
        'length',
        'width',
        'get_content_media_interface',
    ]

    readonly_fields = [
        'get_content_media_interface',
    ]

    inlines = [
        ScheduledSessionInline,
        GymUsageInline,
    ]

    def get_content_media_interface(self, instance: Gymnasium):
        return self.link_display_style_raw(instance.attachments_interface, verbose_name='اینترفیس محتواهای ورزشگاه')

    get_content_media_interface.short_description = 'تصاویر ورزشگاه'



