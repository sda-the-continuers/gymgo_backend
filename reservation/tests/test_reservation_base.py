from typing import List

from gym.models import ScheduledSession
from gym.tests import TestGymBase
from reservation.models import Reserve


class TestReservationBase(TestGymBase):

    def create_reserves(self, scheduled_sessions: List[ScheduledSession]):
        reserves = []
        for ss in scheduled_sessions:
            reserves.append(
                Reserve.objects.create(
                    scheduled_session=ss,
                    gym_usage=ss.gymnasium.gym_usages.first(),
                    athlete=self.athlete,
                )
            )
        return reserves
