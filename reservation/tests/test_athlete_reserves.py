from typing import List

from django.test import tag
from django.utils import timezone

from gym.enums import SCHEDULED_SESSION_STATE_CANCELLED
from gym.models import ScheduledSession
from gym.tests import TEST_GYM_BASE_ATHLETE
from reservation.enums import RESERVE_STATE_PURCHASED, RESERVE_STATE_DONE, RESERVE_STATE_CANCELLED
from reservation.tests import TestReservationBase


@tag('unit_test')
class TestAthleteReserves(TestReservationBase):
    athlete_reserves_url = '/api/reservation/reserve/'
    api_user_type = TEST_GYM_BASE_ATHLETE

    def setUp(self) -> None:
        super().setUp()
        self.gym_complex = self.create_gym_complex()
        self.gymnasium = self.create_gymnasium(self.gym_complex)
        self.gym_usage = self.create_gym_usage(self.gymnasium, type=self.gymnasium.type.sport_types.first())
        self.scheduled_sessions: List[ScheduledSession] = self.create_scheduled_session(
            self.gymnasium,
            (timezone.now() + timezone.timedelta(days=3), timezone.timedelta(hours=1.5), 1),
            (timezone.now() + timezone.timedelta(days=2), timezone.timedelta(hours=1.5), 1),
            (timezone.now() + timezone.timedelta(days=1), timezone.timedelta(hours=1.5), 1),
        )

    def test_athlete_reserves(self):
        self.reserves = self.create_reserves(self.scheduled_sessions)
        resp = self.client.get(
            self.athlete_reserves_url,
            HTTP_AUTHORIZATION=self.jwt_token, data=dict(
                states=[RESERVE_STATE_PURCHASED]
            )
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            [r.id for r in reversed(self.reserves)],
            [r['id'] for r in resp.json()]
        )
        resp = self.client.get(
            self.athlete_reserves_url,
            HTTP_AUTHORIZATION=self.jwt_token, data=dict(
                states=[RESERVE_STATE_DONE, RESERVE_STATE_CANCELLED]
            )
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.json())
        reserve = self.reserves[0]
        reserve.state = RESERVE_STATE_CANCELLED
        reserve.clean()
        reserve.save()
        ss = self.scheduled_sessions[1]
        ss.state = SCHEDULED_SESSION_STATE_CANCELLED
        ss.clean()
        ss.save()
        resp = self.client.get(
            self.athlete_reserves_url,
            HTTP_AUTHORIZATION=self.jwt_token, data=dict(
                states=[RESERVE_STATE_CANCELLED]
            )
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            {r['id'] for r in resp.json()},
            {self.reserves[0].id, self.reserves[1].id}
        )
