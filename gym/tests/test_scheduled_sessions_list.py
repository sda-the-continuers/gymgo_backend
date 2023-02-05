from typing import List

from django.forms.utils import to_current_timezone
from django.test import tag
from django.utils import timezone

from gym.models import ScheduledSession
from gym.tests import TestGymBase, TEST_GYM_BASE_ATHLETE


@tag('unit_test')
class TestScheduledSessionsList(TestGymBase):
    scheduled_session_url = '/api/gym/scheduled-session/'
    api_user_type = TEST_GYM_BASE_ATHLETE

    def setUp(self) -> None:
        super().setUp()
        self.gym_complex = self.create_gym_complex()
        self.gymnasium = self.create_gymnasium(self.gym_complex)
        self.gym_usage = self.create_gym_usage(self.gymnasium, type=self.gymnasium.type.sport_types.first())
        self.scheduled_sessions: List[ScheduledSession] = self.create_scheduled_session(
            self.gymnasium,
            (timezone.now() + timezone.timedelta(days=1), timezone.timedelta(hours=1.5), 3),
            (timezone.now() + timezone.timedelta(days=2), timezone.timedelta(hours=1.5), 2),
            (timezone.now() + timezone.timedelta(days=3), timezone.timedelta(hours=1.5), 5),
        )

    def test_get_scheduled_sessions(self):
        resp = self.client.get(
            self.scheduled_session_url,
            HTTP_AUTHORIZATION=self.jwt_token, data=dict(
                gymnasium=self.gymnasium.id,
                start_datetime__gt=to_current_timezone(self.scheduled_sessions[0].start_datetime)
            )
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 9)
        resp = self.client.get(
            self.scheduled_session_url,
            HTTP_AUTHORIZATION=self.jwt_token, data=dict(
                gym_usage=self.gym_usage.id,
                start_datetime__gt=to_current_timezone(self.scheduled_sessions[2].start_datetime),
                start_datetime__lt=to_current_timezone(self.scheduled_sessions[-2].start_datetime),
            )
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 5)

