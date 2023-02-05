from django.test import tag

from gym.tests import TestRetrieveGymBase


@tag('unit_test')
class TestRetrieveGymComplex(TestRetrieveGymBase):
    retrieve_gym_complex_url = '/api/gym/v2/gym-complex/'

    def test_retrieve_gym_complex_view(self):
        resp = self.client.get(
            f'{self.retrieve_gym_complex_url}{self.gym_complex.id}/',
            HTTP_AUTHORIZATION=self.jwt_token
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data['media']), self.gymnasium_initial_media + self.gym_complex_initial_media)
        self.assertIsNotNone(data['thumbnail']['file'])
        self.assertEqual(data['athlete_reviews']['average_score'], sum(
            [_[0] for _ in self.comments[0] + self.comments[1]]
        ) / (len(self.comments[0])+len(self.comments[1])))
        self.assertEqual(data['athlete_reviews']['reviews_count'], len(self.comments[0])+len(self.comments[1]))
