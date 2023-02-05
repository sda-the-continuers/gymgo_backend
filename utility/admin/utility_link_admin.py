from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from utility.text_processing import make_bold_html


class UtilityLinkAdmin:

    @classmethod
    def get_admin_change_path(cls, obj):
        return reverse('admin:{}_{}_change'.format(obj.meta.app_label, obj.meta.model_name), args=[obj.id])

    @classmethod
    def link_display_style_raw(cls, obj, admin_url=None, verbose_name=None):
        if not obj:
            return '-'
        if verbose_name is None:
            verbose_name = obj.meta.verbose_name
        if admin_url is None:
            admin_url = cls.get_admin_change_path(obj)
        obj_admin = '<a href="{}"target="_blank">مشاهده‌ی {}</a>'.format(
            admin_url, verbose_name
        )
        return format_html(make_bold_html(obj_admin))

    @classmethod
    def link_display_style_detailed(cls, obj, display_attr):
        if not obj:
            return '-'
        obj_admin = '<a href="{}" target="_blank">{}</a>'.format(
            cls.get_admin_change_path(obj), getattr(obj, display_attr)
        )
        return format_html(make_bold_html(obj_admin))

    @classmethod
    def link_display_style_image(cls, obj, obj_id, directory):
        if not obj:
            return '-'
        return format_html(
            '<img src="{media_url}{directory}/{id}/{path}" width=100; height=100; " style="border-radius: 10px;"/>',
            media_url=settings.MEDIA_URL,
            directory=directory,
            id=obj_id,
            path=obj
        )

    @classmethod
    def get_image_html(cls, image_url, width=100, height=100, resize=True):
        if not resize:
            template = u'<img src="{}">'
        else:
            template = u'<img src="{}" width={} height={}>'
        return format_html(
            template.format(
                image_url,
                width,
                height,
            )
        )

    @classmethod
    def link_to_non_origin(cls, url, text):
        return format_html(
            '<a href="{}" target="_blank">{}</a>'.format(
                url, text
            )
        )
