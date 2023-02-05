from django.utils import timezone

from gym.models import GymUsage, ScheduledSession
from gym.tests import TestGymBase, TEST_GYM_BASE_ATHLETE
from reservation.models import Reserve, Comment


class TestRetrieveGymBase(TestGymBase):
    api_user_type = TEST_GYM_BASE_ATHLETE

    comments = [
        [
            (4, 'سلام'),
            (5, 'فلیبگ'),
        ],
        [
            (3, 'سلام'),
            (4, 'فلیبگ'),
        ]
    ]

    gym_complex_initial_media = 2

    gymnasium_initial_media = 3

    def init_comments(self, gym_usage: GymUsage, comments):
        comment_objs = []
        for i, comment in enumerate(comments):
            start = timezone.now() + timezone.timedelta(days=i + 1)
            ss = ScheduledSession.objects.create(
                gymnasium=gym_usage.gymnasium,
                start_datetime=start,
                end_datetime=start + timezone.timedelta(hours=1.5),
                price=500 * 1000,
                gym_owner_price=400 * 1000,
            )
            reserve = Reserve.objects.create(
                scheduled_session=ss, gym_usage=gym_usage, athlete=self.athlete
            )
            comment_objs.append(
                Comment(
                    score=comment[0],
                    comment_text=comment[1],
                    reserve=reserve,
                )
            )
        Comment.objects.bulk_create(comment_objs)

    def setUp(self) -> None:
        super().setUp()
        self.gym_complex = self.create_gym_complex(initial_media=self.gym_complex_initial_media)
        self.gymnasium = self.create_gymnasium(self.gym_complex, initial_media=self.gymnasium_initial_media)
        self.gym_usage1 = self.create_gym_usage(self.gymnasium, type=self.gymnasium.type.sport_types.first())
        self.gym_usage2 = self.create_gym_usage(self.gymnasium, type=self.gymnasium.type.sport_types.last())
        self.init_comments(self.gym_usage1, self.comments[0])
        self.init_comments(self.gym_usage2, self.comments[1])
