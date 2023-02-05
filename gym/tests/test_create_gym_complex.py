from django.test import tag

from gym.models import GymnasiumType, GymnasiumAttribute, SportType, GymComplex, Gymnasium
from gym.tests import TestGymBase, TEST_GYM_BASE_GYM_OWNER


@tag('unit_test')
class TestCreateGymComplex(TestGymBase):
    gym_owner_gym_complex_create_url = '/api/gym/gym-complex/'
    api_user_type = TEST_GYM_BASE_GYM_OWNER
    should_create_gymnasium_attributes = True

    def test_normal_create(self):
        thumbnails, media = self.create_free_content_media(thumbnail_number=2, media_number=5)
        data = {
            'phone_number': '09393939393',
            'name': 'شکلات شیری',
            'owner': self.gym_owner.id,
            'address': 'استادمعین اولاش',
            'description': 'توضیحات نداره',
            'rules': 'حجاب اختیاری',
            'instagram_username': 'leomessi',
            'gymnasiums': [
                {
                    'type': GymnasiumType.objects.get(title_fa='سالن').id,
                    'description': 'الکی',
                    'rules': 'مشابه قوانین مجموعه',
                    'length': 85,
                    'width': 85,
                    'attributes': list(GymnasiumAttribute.objects.values_list('id', flat=True)[:5]),
                    'gym_usages': [
                        {
                            'type': SportType.objects.get(title_fa='فوتبال').id,
                            'equipments': [
                                {
                                    'type': 'BALL',
                                    'price': 20 * 1000,
                                },
                            ]
                        },
                        {
                            'type': SportType.objects.get(title_fa='بسکتبال').id,
                        },
                    ],
                    'set_media': [medium.id for medium in media[2:]],
                    'set_thumbnail': thumbnails[1].id
                }, {
                    'type': GymnasiumType.objects.get(title_fa='استخر').id,
                    'description': 'الکی‌تر',
                    'rules': 'مشابه قوانین مجموعه نیست این یکی',
                    'length': 100,
                    'width': 100,
                    'attributes': list(GymnasiumAttribute.objects.values_list('id', flat=True)[:3]),
                    'gym_usages': [
                        {
                            'type': SportType.objects.get(title_fa='شنا').id,
                        },
                    ],
                },
            ],
            'nicknames': [
                {'nickname': 'الکی‌کده'},
                {'nickname': 'آزاد‌راه'},
            ],
            'set_media': [medium.id for medium in media[:2]],
            'set_thumbnail': thumbnails[0].id
        }
        resp = self.client.post(
            self.gym_owner_gym_complex_create_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data=data, format='json'
        )
        self.assertTrue(str(resp.status_code).startswith("2"), msg=resp.json())
        gym_complex = GymComplex.objects.get(id=resp.json()['id'])
        gymnasium1: Gymnasium = gym_complex.gymnasiums.first()
        gymnasium2: Gymnasium = gym_complex.gymnasiums.last()
        self.assertIsNotNone(gym_complex.thumbnail)
        expected, real = (
            {True, False},
            {gymnasium1.thumbnail is None, gymnasium2.thumbnail is None}
        )
        self.assertEqual(
            expected, real, msg=f'expected: {expected}, real: {real}'
        )
        self.assertEqual(gym_complex.media.count(), 2)
        self.assertEqual({gymnasium1.media.count(), gymnasium2.media.count()}, {3, 0})
        expected, real = {5, 3}, {gymnasium1.attributes.count(), gymnasium2.attributes.count()}
        self.assertEqual(expected, real, msg=f'expected: {expected}, real: {real}')
        self.assertEqual(gym_complex.nicknames.count(), 2)
