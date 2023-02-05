from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.html import format_html
from jalali_date.admin import ModelAdminJalaliMixin

from account.admin import AccountAdmin
from account.models import Athlete, ProfilePicture, AthleteReferral
from utility.admin.utility_link_admin import UtilityLinkAdmin
from utility.text_processing import jalali_strfdate


class ProfilePictureInline(UtilityLinkAdmin, TabularInline):
    model = ProfilePicture
    fields = [
        'get_file',
        'file',
        'is_active',
    ]

    readonly_fields = [
        'get_file',
    ]
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(is_active=False)

    def get_file(self, instance: ProfilePicture):
        if instance.file:
            return self.get_image_html(instance.file.url, 300, 300)
        return '---'

    def has_delete_permission(self, request, obj=None):
        return False

    get_file.short_description = 'نمایش عکس پروفایل'


class ReferInlineBase(UtilityLinkAdmin, TabularInline):
    model = AthleteReferral
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ReferrerInline(ReferInlineBase):
    fields = [
        'get_referrer',
    ]
    readonly_fields = [
        'get_referrer',
    ]
    fk_name = 'referred_athlete'

    def get_referrer(self, instance: AthleteReferral):
        return self.link_display_style_raw(instance.referrer_athlete)

    get_referrer.short_description = 'ورزشکار معرفی کننده'


class ReferredInline(ReferInlineBase):
    fields = [
        'get_referred',
    ]
    readonly_fields = [
        'get_referred',
    ]
    fk_name = 'referrer_athlete'

    def get_referred(self, instance: AthleteReferral):
        return self.link_display_style_raw(instance.referred_athlete)

    get_referred.short_description = 'ورزشکار معرفی شده'


@admin.register(Athlete)
class AthleteAdmin(ModelAdminJalaliMixin, AccountAdmin):
    list_display_links = [
        'id', 'get_profile_picture'
    ]

    list_display = [
        'id',
        'get_profile_picture',
        'phone_number',
        'full_name',
        'gender',
        'get_birth_date',
    ]

    fieldsets = [
        *AccountAdmin.fieldsets,
        (
            'اطلاعات ورزشکاری', {
                'fields': (
                    'phone_number',
                    'get_profile_picture',
                    'gender',
                    'birth_date',
                    'favorite_sports',
                    'referral_code',
                )
            }
        )
    ]

    readonly_fields = [
        *AccountAdmin.readonly_fields,
        'referral_code',
        'get_profile_picture',
    ]

    inlines = [
        ProfilePictureInline,
        ReferrerInline,
        ReferredInline,
    ]

    @admin.display(description='تاریخ تولد')
    def get_birth_date(self, obj):
        return jalali_strfdate(obj.birth_date)

    def get_profile_picture(self, instance: Athlete):
        if profile_picture := instance.profile_picture:
            return self.get_image_html(profile_picture.file.url, 125, 125)
        return '---'

    get_profile_picture.short_description = 'عکس پروفایل'
