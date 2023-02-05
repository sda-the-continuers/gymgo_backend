import typing
from dataclasses import dataclass

from django.utils import timezone

if typing.TYPE_CHECKING:
    from account.models import Athlete
    from gym.models import ScheduledSession, GymUsage
    from discount.models import DiscountRestriction


@dataclass
class DiscountApplierComponent:
    athlete: 'Athlete'
    scheduled_session: 'ScheduledSession'
    gym_usage: 'GymUsage'


class RestrictionData:
    def __init__(
            self,
            discount_restriction: 'DiscountRestriction',
            athlete: 'Athlete',
            scheduled_session: 'ScheduledSession',
            gym_usage: 'GymUsage'
    ):
        self.discount_restriction = discount_restriction
        super().__init__(athlete, scheduled_session, gym_usage)

    @classmethod
    def from_discount_applier_component(
            cls, discount_restriction: 'DiscountRestriction', component: DiscountApplierComponent
    ):
        return cls(discount_restriction, component.athlete, component.scheduled_session, component.gym_usage)

    @property
    def now(self):
        return timezone.now()

    @property
    def repeats(self):
        from reservation.models import Reserve
        from reservation.enums import RESERVE_STATE_CANCELLED
        return Reserve.objects.exclude(
            state=RESERVE_STATE_CANCELLED
        ).filter(discount_id=self.discount_restriction.discount_id).count()
