from django.db.models import QuerySet

from discount.models import AthleteBasedDiscount
from gym.models.club import ClubRelatedMixin


class ClubDiscount(ClubRelatedMixin, AthleteBasedDiscount):

    def can_apply_athlete(self, athlete) -> bool:
        # overriden due to better query performance
        return self.contacts.filter(athlete_id=athlete.id).exists()

    @property
    def athletes_that_can_apply(self) -> QuerySet:
        from account.models import Athlete
        return Athlete.objects.filter(id__in=self.contacts.values_list('athlete_id', flat=True))

    class Meta:
        verbose_name = 'تخفیف باشگاه مخاطبین'
        verbose_name_plural = 'تخفیف‌های باشگاه‌های مخاطبین'
