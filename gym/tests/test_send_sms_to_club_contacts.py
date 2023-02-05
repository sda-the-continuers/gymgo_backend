import copy

from django.test import tag
from django.utils import timezone

from account.models import GymOwner
from discount.models import IntegerDiscountRestriction, DateTimeDiscountRestriction
from gym.models import ClubSMS, ClubDiscount
from gym.tests import TestGymBase, TEST_GYM_BASE_GYM_OWNER


@tag('unit_test')
class TestSendSMSToClubContacts(TestGymBase):
    api_user_type = TEST_GYM_BASE_GYM_OWNER
    club_sms_url = '/api/gym/club-sms/'

    def setUp(self) -> None:
        super().setUp()
        self.gym_complex = self.create_gym_complex(has_thumbnail=False)
        self.other_gym_owner = GymOwner.objects.create(
            phone_number='09381111111',
            full_name='unit-test2'
        )
        self.other_gym_complex = self.create_gym_complex(has_thumbnail=False, owner=self.other_gym_owner)
        self.club_contacts = self.create_club_contacts(self.gym_complex)
        self.other_club_contacts = self.create_club_contacts(self.other_gym_complex)

    def test_send_sms_to_club_contacts(self):
        self.assertFalse(ClubSMS.objects.filter(club=self.gym_complex.club).exists())
        resp = self.client.post(
            self.club_sms_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data={
                'club': self.gym_complex.club_id,
                'contacts': [contact.id for contact in self.club_contacts],
                'message': 'this is a test',
            }
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(ClubSMS.objects.filter(club=self.gym_complex.club).exists())
        resp = self.client.post(
            self.club_sms_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data={
                'club': self.gym_complex.club_id,
                'contacts': [contact.id for contact in self.club_contacts] + [self.other_club_contacts[0].id],
                'message': 'this is another test',
            }
        )
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(ClubSMS.objects.filter(club=self.gym_complex.club, message='this is another test').exists())


@tag('unit_test')
class TestSendSMSForDiscountToClubContacts(TestSendSMSToClubContacts):
    club_sms_url = '/api/gym/club-discount-sms/'

    def test_send_sms_to_club_contacts(self):
        data = {
            'club': self.gym_complex.club_id,
            'contacts': [contact.id for contact in self.club_contacts],
            'message': 'this is a test',
            'discount': {
                'code': 'test-code',
                'general_pricing_type': {
                    'discount_percentage_amount': 25,
                    'maximum_discount_amount': 100000,
                },
                'club': self.gym_complex.club_id,
                'contacts': [cc.id for cc in self.club_contacts[:-1]]
            }
        }
        resp = self.client.post(
            self.club_sms_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data=data, format='json'
        )
        self.assertEqual(resp.status_code, 201)
        cd: ClubDiscount = ClubDiscount.objects.last()
        cs: ClubSMS = ClubSMS.objects.last()
        self.assertEqual(set(cd.contacts.values_list('id', flat=1)), set(cs.contacts.values_list('id', flat=1)))
        new_data = copy.deepcopy(data)
        new_data['discount']['general_pricing_type']['discount_amount'] = 100000
        resp = self.client.post(
            self.club_sms_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data=new_data, format='json'
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('یک نوع تخفیف', resp.json()['discount_percentage_amount'][0])
        new_data = copy.deepcopy(data)
        new_data['discount']['general_pricing_type'] = {}
        resp = self.client.post(
            self.club_sms_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data=new_data, format='json'
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('یک نوع تخفیف', resp.json()['discount_percentage_amount'][0])
        new_data = copy.deepcopy(data)
        new_data['discount']['until'] = timezone.now() + timezone.timedelta(days=10)
        new_data['discount']['repeats'] = 2
        resp = self.client.post(
            self.club_sms_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            data=new_data, format='json'
        )
        self.assertEqual(resp.status_code, 201, msg=resp.json())
        cd: ClubDiscount = ClubDiscount.objects.last()
        self.assertEqual(
            set(restriction.__class__ for restriction in cd.restrictions),
            {DateTimeDiscountRestriction, IntegerDiscountRestriction}
        )
