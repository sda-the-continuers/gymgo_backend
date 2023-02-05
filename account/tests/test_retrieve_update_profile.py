import json

from django.test import tag
from django.core.files import File

from account.models import ProfilePicture
from utility.enums import SAMPLE_IMAGE_PATH
from utility.tests import AthleteTestCase


@tag('unit_test')
class TestRetrieveUpdateProfile(AthleteTestCase):
    retrieve_athlete_url = '/api/account/athlete/profile/'
    retrieve_profile_picture_url = '/api/account/profile-picture/'

    def setUp(self) -> None:
        super().setUp()
        with open(SAMPLE_IMAGE_PATH, mode='rb') as f:
            ProfilePicture.objects.create(
                account=self.athlete,
                file=File(f),
                is_active=True
            )

    def test_retrieve_profile(self):
        resp = self.client.get(
            self.retrieve_athlete_url,
            HTTP_AUTHORIZATION=self.jwt_token
        )
        data = resp.json()
        self.assertEqual(data["profile_picture"]["id"], self.athlete.profile_picture.id)
        self.assertEqual(data['phone_number'], self.athlete.phone_number)
        profile_picture_data = self.client.get(
            f'{self.retrieve_profile_picture_url}{data["profile_picture"]["id"]}/',
            HTTP_AUTHORIZATION=self.jwt_token
        ).json()
        self.assertEqual(profile_picture_data["id"], data["profile_picture"]["id"])

    def test_update_profile_picture(self):
        previous_profile_picture_id = self.athlete.profile_picture.id
        with open(SAMPLE_IMAGE_PATH, mode='rb') as f:
            content_media_response = self.client.post(
                self.retrieve_profile_picture_url, HTTP_AUTHORIZATION=self.jwt_token, data={
                    'file': f,
                    'account': self.athlete.id,
                }
            ).json()
        self.assertEqual(previous_profile_picture_id, self.athlete.profile_picture.id)
        self.assertFalse(ProfilePicture.objects.get(id=content_media_response['id']).is_active)
        self.client.patch(
            self.retrieve_athlete_url, HTTP_AUTHORIZATION=self.jwt_token, data={
                'full_name': 'اصغر',
                'set_profile_picture': content_media_response['id'],
            }
        )
        self.assertNotEqual(previous_profile_picture_id, self.athlete.profile_picture.id)
        self.assertTrue(ProfilePicture.objects.get(id=content_media_response['id']).is_active)
        self.client.patch(
            self.retrieve_athlete_url, HTTP_AUTHORIZATION=self.jwt_token, data={
                'full_name': 'اکبر',
            }
        )
        self.assertTrue(ProfilePicture.objects.get(id=content_media_response['id']).is_active)
        resp = self.client.patch(
            self.retrieve_athlete_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data=json.dumps({
                'full_name': 'اکبر',
                'set_profile_picture': None
            }),
            content_type="application/json"
        )
        self.assertFalse(str(resp.status_code).startswith("4"))
        self.assertIsNone(self.athlete.profile_picture)
