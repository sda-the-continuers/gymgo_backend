from rest_framework.test import APITestCase

from account.jwt import get_jwt_token
from account.models import Athlete


class UserTestCase(APITestCase):

    @staticmethod
    def get_jwt_token(athlete):
        access = get_jwt_token(athlete)[-1]
        return f'JWT {access}'


class AthleteTestCase(UserTestCase):

    def setUp(self) -> None:
        self.athlete = Athlete.objects.create(
            phone_number='09391111111',
            full_name='unit+test'
        )
        self.jwt_token = self.get_jwt_token(self.athlete)
