from typing import Type, Tuple, List

from django.core.files import File
from django.db.models import Q

from account.models import Athlete, GymOwner
from gym.fixes import create_gymnasium_attributes
from gym.models import GymComplex, GymThumbnail, GymContentMediaMixin, Gymnasium, SportType, GymnasiumType, GymUsage, \
    GymContentMedia, ScheduledSession, ClubContact
from utility.enums import SAMPLE_IMAGE_PATH
from utility.models import EnumBaseModel
from utility.tests import UserTestCase

TEST_GYM_BASE_ATHLETE = 'ATHLETE'
TEST_GYM_BASE_GYM_OWNER = 'GYM_OWNER'


class TestGymBase(UserTestCase):
    sport_types = [
        ('football', 'فوتبال'),
        ('basketball', 'بسکتبال'),
        ('volleyball', 'والیبال'),
        ('swim', 'شنا'),
    ]

    gymnasium_types = [
        ('Salon', 'سالن', ['football', 'basketball', 'volleyball']),
        ('pool', 'استخر', ['swim']),
    ]

    raw_club_contacts = [
        ('علیرضا اچ‌زد', '09112233344'),
        ('پارسا افصحی', '09223344455'),
    ]

    api_user_type = None
    should_create_sport_types = True
    should_create_gymnasium_attributes = False

    def init_types(self):
        for sport_type in self.sport_types:
            SportType.objects.create(title=sport_type[0], title_fa=sport_type[1])
        for gymnasium_type in self.gymnasium_types:
            gt: GymnasiumType = GymnasiumType.objects.create(title=gymnasium_type[0], title_fa=gymnasium_type[1])
            gt.sport_types.set(SportType.objects.filter(title__in=gymnasium_type[2]))

    def setUp(self) -> None:
        self.athlete = Athlete.objects.create(
            phone_number='09391111111',
            full_name='unit+test'
        )
        self.gym_owner = GymOwner.objects.create(
            phone_number='09391111111',
            full_name='unit-test'
        )
        if self.should_create_sport_types:
            self.init_types()
        if self.should_create_gymnasium_attributes:
            create_gymnasium_attributes()
        {
            TEST_GYM_BASE_ATHLETE: self.be_athlete,
            TEST_GYM_BASE_GYM_OWNER: self.be_gym_owner,
        }.get(self.api_user_type, lambda: 1)()

    @staticmethod
    def create_free_content_media(*, thumbnail_number=0, media_number=0) -> Tuple[
        List[GymThumbnail], List[GymContentMedia]
    ]:
        thumbnails, media = [], []
        with open(SAMPLE_IMAGE_PATH, mode='rb') as f:
            for _ in range(thumbnail_number):
                thumbnails.append(GymThumbnail(file=File(f)))
            for _ in range(media_number):
                media.append(GymContentMedia(file=File(f)))
            _, __ = GymThumbnail.objects.bulk_create(thumbnails), GymContentMedia.objects.bulk_create(media)
        return _, __

    @staticmethod
    def create_content_media(gym: GymContentMediaMixin, has_thumbnail, initial_media):
        if has_thumbnail or initial_media > 0:
            with open(SAMPLE_IMAGE_PATH, mode='rb') as f:
                if has_thumbnail:
                    GymThumbnail.objects.create(
                        attachments_interface=gym.attachments_interface,
                        file=File(f)
                    )
                media = []
                for _ in range(initial_media):
                    media.append(
                        GymContentMedia(
                            attachments_interface=gym.attachments_interface,
                            file=File(f)
                        )
                    )
                GymContentMedia.objects.bulk_create(media)

    def create_gym_complex(self, has_thumbnail=True, initial_media=0, **create_kwargs):
        default_kwargs = dict(
            phone_number=self.gym_owner.phone_number,
            name='فدک',
            owner=self.gym_owner,
            address='فدک',
        )
        default_kwargs.update(create_kwargs)
        gym_complex = GymComplex.objects.create(**default_kwargs)
        self.create_content_media(gym_complex, has_thumbnail, initial_media)
        return gym_complex

    def create_gymnasium(self, gym_complex: GymComplex, has_thumbnail=False, initial_media=1, **create_kwargs):
        default_kwargs = dict(
            gym_complex=gym_complex,
            type=GymnasiumType.objects.first(),
            length=85,
            width=85,
        )
        default_kwargs.update(create_kwargs)
        gymnasium = Gymnasium.objects.create(**default_kwargs)
        self.create_content_media(gymnasium, has_thumbnail, initial_media)
        return gymnasium

    def create_gym_usage(self, gymnasium: Gymnasium, **create_kwargs):
        default_kwargs = dict(
            gymnasium=gymnasium,
            type=SportType.objects.first(),
        )
        default_kwargs.update(create_kwargs)
        return GymUsage.objects.create(**default_kwargs)

    def create_scheduled_session(self, gymnasium: Gymnasium, *light_schedule_sessions, **create_kwargs):
        scheduled_sessions = []
        default_kwargs = dict(
            price=500 * 1000,
            gym_owner_price=400 * 1000,
        )
        default_kwargs.update(create_kwargs)
        for start_datetime, timedelta, steps in light_schedule_sessions:
            datetime_ = start_datetime
            for _ in range(steps):
                final_kwargs = dict(
                    gymnasium=gymnasium,
                    start_datetime=datetime_,
                    end_datetime=datetime_ + timedelta,
                    **default_kwargs
                )
                scheduled_sessions.append(ScheduledSession(**final_kwargs))
                datetime_ += timedelta
        scheduled_sessions = ScheduledSession.objects.bulk_create(scheduled_sessions)
        return scheduled_sessions

    def be_athlete(self):
        self.jwt_token = self.get_jwt_token(self.athlete)

    def be_gym_owner(self):
        self.jwt_token = self.get_jwt_token(self.gym_owner)

    @staticmethod
    def get_type(type_class: Type[EnumBaseModel], title):
        type_ = type_class.objects.filter(Q(title=title) | Q(title_fa=title)).first()
        if not type_:
            raise type_class.DoesNotExist(f'sport type with title {title} does not exists')
        return type_

    @classmethod
    def get_sport_type(cls, title):
        return cls.get_type(SportType, title)

    @classmethod
    def get_gymnasium_type(cls, title):
        return cls.get_type(GymnasiumType, title)

    def create_club_contacts(self, gym_complex: GymComplex, club_contacts: List[Tuple[str, str]] = None,
                             **create_kwargs):
        club_contacts = club_contacts or self.raw_club_contacts
        default_kwargs = dict(
            club=gym_complex.club,
        )
        default_kwargs.update(create_kwargs)
        contacts = []
        for name, number in club_contacts:
            contacts.append(
                ClubContact(
                    full_name=name,
                    phone_number=number,
                    **default_kwargs,
                )
            )
        return ClubContact.objects.bulk_create(contacts)
