from typing import Union, TYPE_CHECKING

from django.db import models

from utility.models import BaseModel, CreateHistoryModel

if TYPE_CHECKING:
    from gym.models import GymComplex, Gymnasium


def get_gym_content_media_upload_to(instance: 'GymContentMediaBase', filename):
    base_url = 'gym'
    if instance.attachments_interface:
        base_url = f'{base_url}/{instance.attachments_interface.concrete_gym.id}'
    return f'{base_url}/{filename}'


class GymContentMediaBase(CreateHistoryModel):
    file = models.FileField(
        upload_to=get_gym_content_media_upload_to,
        verbose_name='فایل',
    )

    attachments_interface: 'GymContentMediaInterface' = None

    class Meta:
        abstract = True


class GymContentMedia(GymContentMediaBase):
    attachments_interface = models.ForeignKey(
        to='GymContentMediaInterface',
        on_delete=models.CASCADE,
        related_name='media',
        verbose_name='رابط ضمیمه',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'عکس ورزشگاه'
        verbose_name_plural = 'عکس‌های ورزشگاه'


class GymThumbnail(GymContentMediaBase):
    attachments_interface = models.OneToOneField(
        to='GymContentMediaInterface',
        on_delete=models.CASCADE,
        related_name='thumbnail',
        verbose_name='رابط ضمیمه',
        null=True, blank=True,
    )


class GymContentMediaInterface(BaseModel):

    @property
    def try_gymnasium(self):
        from gym.models import Gymnasium
        if isinstance(self, Gymnasium):
            return self
        try:
            return self.gymnasium
        except:
            return None

    @property
    def try_gym_complex(self):
        from gym.models import GymComplex
        if isinstance(self, GymComplex):
            return self
        try:
            return self.gymcomplex
        except:
            return None

    @property
    def concrete_gym(self) -> Union['GymComplex', 'Gymnasium']:
        return self.try_gym_complex or self.try_gymnasium


class GymContentMediaMixin(models.Model):
    attachments_interface = models.OneToOneField(
        to='GymContentMediaInterface',
        on_delete=models.CASCADE,
        verbose_name='پیوست‌ها',
    )

    def before_create(self):
        self.attachments_interface = GymContentMediaInterface.objects.create()

    @property
    def thumbnail(self):
        if self.attachments_interface:
            return GymThumbnail.objects.filter(attachments_interface=self.attachments_interface).first()

    @property
    def media(self):
        if self.attachments_interface:
            return GymContentMedia.objects.filter(attachments_interface=self.attachments_interface)

    class Meta:
        abstract = True
