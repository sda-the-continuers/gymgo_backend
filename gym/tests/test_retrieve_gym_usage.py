from django.test import tag

from gym.tests import TestRetrieveGymBase


@tag('unit_test')
class TestRetrieveGymUsage(TestRetrieveGymBase):
    retrieve_gym_usage_url = '/api/gym/gym-usage/'

    def test_retrieve_gym_complex_view(self):
        resp = self.client.get(
            f'{self.retrieve_gym_usage_url}{self.gym_usage1.id}/',
            HTTP_AUTHORIZATION=self.jwt_token
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data['gymnasium']['media']), self.gymnasium_initial_media)
        self.assertEqual(data['athlete_reviews']['average_score'], sum(
            [_[0] for _ in self.comments[0]]
        ) / len(self.comments[0]))
        self.assertEqual(data['athlete_reviews']['reviews_count'], len(self.comments[0]))
