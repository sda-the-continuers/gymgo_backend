from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from account.enums import ACCOUNT_TYPE_ATHLETE, ACCOUNT_TYPE_GYM_OWNER
from account.models import Athlete, GymOwner
from account.models.athlete_referral import AthleteReferral
from gymtime_backend.settings import SMS_EXPIRATION_MINUTES
from sms.enums import SMS_USAGE_TYPE_LOGIN, SMS_USAGE_TYPE_SIGNUP
from sms.models import SMSVerification
from utility.mixins import PhoneNumberSerializer


class BaseAccountSMSEntrySerializer(PhoneNumberSerializer, Serializer):
    sms_token = serializers.CharField(max_length=16)
    usage_type = None
    account_type = None

    def check_sms_token_validity(self, attrs):
        if not SMSVerification.objects.filter(
            token=attrs['sms_token'],
            phone_number=attrs['phone_number'],
            usage_type=self.usage_type,
            account_type=self.account_type,
            is_used=False,
            created__gt=timezone.now() - timezone.timedelta(minutes=SMS_EXPIRATION_MINUTES)
        ).exists():
            raise ValidationError({
                'sms_token': 'کد وارد شده صحیح نیست یا منقضی شده است'
            })

    def phone_number_exists(self, phone_number):
        model = self.__class__.Meta.model
        return model.objects.filter(phone_number=phone_number).exists()

    def check_phone_number_existence(self, phone_number):
        if not self.phone_number_exists(phone_number):
            raise ValidationError({
                'phone_number': 'شماره همراه وارد شده قبلا استفاده نشده است'
            })

    def check_phone_number_nonexistence(self, phone_number):
        if self.phone_number_exists(phone_number):
            raise ValidationError({
                'phone_number': 'شماره همراه وارد شده قبلا استفاده شده است'
            })

    def validate(self, attrs):
        self.check_sms_token_validity(attrs)
        if self.usage_type == SMS_USAGE_TYPE_LOGIN:
            self.check_phone_number_existence(attrs['phone_number'])
        elif self.usage_type == SMS_USAGE_TYPE_SIGNUP:
            self.check_phone_number_nonexistence(attrs['phone_number'])
        self.context['sms_token'] = attrs.pop('sms_token')
        return attrs

    class Meta:
        model = None
        fields = []


class AthleteLoginSerializer(BaseAccountSMSEntrySerializer):
    usage_type = SMS_USAGE_TYPE_LOGIN
    account_type = ACCOUNT_TYPE_ATHLETE

    class Meta:
        model = Athlete
        fields = [
            'phone_number',
            'sms_token'
        ]


class AthleteSignupSerializer(BaseAccountSMSEntrySerializer, ModelSerializer):
    referral_code = serializers.CharField(max_length=16, required=False, write_only=True)
    usage_type = SMS_USAGE_TYPE_SIGNUP
    account_type = ACCOUNT_TYPE_ATHLETE

    def create(self, validated_data):
        with transaction.atomic():
            referral_code = validated_data.pop('referral_code', '')
            athlete = super().create(validated_data)
            try:
                referrer_athlete = Athlete.objects.get(referral_code=referral_code)
                AthleteReferral.objects.create(referred_athlete=athlete, referrer_athlete=referrer_athlete)
            except Athlete.DoesNotExist:
                pass
        return athlete

    class Meta:
        model = Athlete
        fields = [
            'phone_number',
            'sms_token',
            'referral_code'
        ]


class GymOwnerLoginSerializer(BaseAccountSMSEntrySerializer):
    usage_type = SMS_USAGE_TYPE_LOGIN
    account_type = ACCOUNT_TYPE_GYM_OWNER

    class Meta:
        model = GymOwner
        fields = [
            'phone_number',
            'sms_token'
        ]


class GymOwnerSignUpSerializer(BaseAccountSMSEntrySerializer, ModelSerializer):
    full_name = serializers.CharField(max_length=32)
    usage_type = SMS_USAGE_TYPE_SIGNUP
    account_type = ACCOUNT_TYPE_GYM_OWNER

    class Meta:
        model = GymOwner
        fields = [
            'full_name',
            'phone_number',
            'sms_token',
        ]


