from django.db import models

from utility.models import HistoricalBaseModel


class GymUsage(HistoricalBaseModel):

    gymnasium = models.ForeignKey(
        to='gym.Gymnasium',
        on_delete=models.CASCADE,
        related_name='gym_usages',
        verbose_name='ورزشگاه مربوطه',
    )

    type = models.ForeignKey(
        to='gym.SportType',
        on_delete=models.PROTECT,
        related_name='gym_usages',
        verbose_name='نوع ورزش',
    )

    @property
    def comments(self):
        from reservation.models import Comment
        return Comment.get_comments_for_gym(self)

    def before_create(self):
        if not self.type.gymnasium_types.filter(id=self.gymnasium.type.id).exists():
            raise ValueError({'type': 'این ورزش برای این سرویس ورزشی نیست؟'})

    class Meta:
        verbose_name = 'کاربری ورزشگاه'
        verbose_name_plural = 'کاربری‌های ورزشگاه'
