from django.core.files import File
from django.test import tag

from gym.models import SportType, SportTypeIcon
from utility.enums import SAMPLE_IMAGE_PATH
from utility.tests import AthleteTestCase


@tag('unit_test')
class TestSelectFavoriteSports(AthleteTestCase):
    favorite_sports_url = '/api/gym/favorite-sports/'
    sport_types = [
        ('football', 'فوتبال'),
        ('basketball', 'بسکتبال'),
        ('volleyball', 'والیبال')
    ]

    def set_sport_types(self):
        types = []
        for title, title_fa in self.sport_types:
            types.append(SportType(title=title, title_fa=title_fa))
        SportType.objects.bulk_create(types)

    def setUp(self) -> None:
        super().setUp()
        self.set_sport_types()

    def test_get_sport_types(self):
        with open(SAMPLE_IMAGE_PATH, mode='rb') as f:
            SportTypeIcon.objects.create(
                sport_type=SportType.objects.first(),
                file=File(f)
            )
            err_resp = self.client.get(self.favorite_sports_url)
            self.assertEqual(err_resp.status_code, 401)
            resp = self.client.get(
                self.favorite_sports_url,
                HTTP_AUTHORIZATION=self.jwt_token
            )
            self.assertEqual(len(resp.json()), 3)
            self.assertEqual(set(sport_type['title'] for sport_type in resp.json()), set(
                dict(self.sport_types).keys()
            ))
            self.assertIsNotNone(
                resp.json()[0]['icon']
            )

    def test_select_favorite_sports(self):
        sport_type_ids = list(SportType.objects.order_by('id').values_list('id', flat=True))
        selected_ids = [sport_type_ids[0], sport_type_ids[-1] + 2, sport_type_ids[-1]]
        resp = self.client.patch(
            self.favorite_sports_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data=dict(favorite_sports=selected_ids),
        )
        self.assertEqual(resp.status_code, 400)
        selected_ids = [sport_type_ids[0], sport_type_ids[-1]]
        resp = self.client.patch(
            self.favorite_sports_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data=dict(favorite_sports=selected_ids),
        )
        self.assertEqual(resp.status_code, 200)
        self.athlete.refresh_from_db()
        self.assertEqual(set(selected_ids), set(self.athlete.favorite_sports.values_list('id', flat=1)))
