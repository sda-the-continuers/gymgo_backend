from urllib.parse import urljoin

from django.contrib import admin
from django.utils.html import format_html
from nested_admin.nested import NestedModelAdmin

from gym.admin.gym_complex import GymnasiumInline
from gym.models import GymComplex
from utility.admin.utility_link_admin import UtilityLinkAdmin
from utility.enums import INSTAGRAM_ROOT


@admin.register(GymComplex)
class GymComplexAdmin(UtilityLinkAdmin, NestedModelAdmin):
    inlines = [
        GymnasiumInline,
    ]

    list_display = [
        'id',
        'get_thumbnail_image',
        'code',
        'name',
        'get_owner',
        'phone_number',
        'address',
    ]

    fieldsets = [
        (None, {
            'fields': (
                'get_thumbnail_image',
                'code',
                'name',
                'owner',
                'get_owner',
                'get_content_media_interface',
            ),
        }),
        (
            'ارتباطات و قوانین', {
                'fields': (
                    'phone_number',
                    'address',
                    'instagram_username',
                    'get_instagram_page',
                    'description',
                    'rules',
                    'get_club',
                )
            }
        ),
    ]

    readonly_fields = [
        'id', 'get_thumbnail_image', 'get_owner', 'get_club', 'get_instagram_page', 'get_content_media_interface'
    ]

    def get_owner(self, instance: GymComplex):
        return self.link_display_style_raw(instance.owner)

    get_owner.short_description = GymComplex.get_field('owner').verbose_name

    def get_club(self, instance: GymComplex):
        return self.link_display_style_raw(instance.club)

    get_club.short_description = GymComplex.get_field('club').verbose_name

    def get_instagram_page(self, instance: GymComplex):
        return self.link_to_non_origin(
            urljoin(INSTAGRAM_ROOT, instance.instagram_username), instance.instagram_username
        )

    get_instagram_page.short_description = GymComplex.get_field('instagram_username').verbose_name

    def get_thumbnail_image(self, instance: GymComplex):
        if not instance.thumbnail:
            return '---'
        return self.get_image_html(
            instance.thumbnail.file.url, resize=False,
        )

    get_thumbnail_image.short_description = 'تصویر اصلی'

    def get_content_media_interface(self, instance: GymComplex):
        return self.link_display_style_raw(
            instance.attachments_interface, verbose_name='اینترفیس محتواهای مجموعه ورزشی'
        )

    get_content_media_interface.short_description = 'تصاویر مجموعه'
