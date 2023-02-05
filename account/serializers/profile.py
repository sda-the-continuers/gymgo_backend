from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from account.models import Athlete, Account, GymOwner, ProfilePicture
from gym.serializers import FavoriteSportsSerializer


class AccountProfileSerializer(ModelSerializer):
    set_profile_picture = serializers.IntegerField(min_value=1, required=True, write_only=True, allow_null=True)
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, instance):
        return ProfilePictureSerializer(
            instance.profile_picture,
            allow_null=True,
            context=self.context,
        ).data

    def _set_profile_picture(self, instance: Account, profile_picture_id):
        if profile_picture_id is not None and not instance.profile_pictures.filter(id=profile_picture_id).exists():
            raise ValidationError({'set_profile_picture': ['عکس پروفایل با این آیدی وجود ندارد']})
        if profile_picture_id:
            instance.profile_pictures.filter(id=profile_picture_id).update(is_active=True)
        instance.profile_pictures.exclude(id=profile_picture_id).update(is_active=False)

    def update(self, instance, validated_data):
        with transaction.atomic():
            if 'set_profile_picture' in validated_data:
                self._set_profile_picture(instance, validated_data.pop('set_profile_picture'))
            return super().update(instance, validated_data)

    class Meta:
        model = Account
        fields = [
            'id',
            'full_name',
            'phone_number',
            'user',
            'wallet',
            'crm_account',
            'account_type',
            'set_profile_picture',
            'profile_picture',
        ]


class AthleteProfileSerializer(AccountProfileSerializer):
    favorite_sports = FavoriteSportsSerializer(many=True)
    jalali_birth_date = serializers.DateField(read_only=True)

    class Meta:
        model = Athlete
        fields = [
            'gender',
            'birth_date',
            'jalali_birth_date',
            'favorite_sports',
            *AccountProfileSerializer.Meta.fields,
        ]


class GymOwnerProfileSerializer(AccountProfileSerializer):

    def validate_shaba(self, shaba):
        if len(shaba) != 24:
            raise ValidationError({
                'shaba': 'شماره شبا باید ۲۴ رقمی باشد'
            })
        return shaba

    class Meta:
        model = GymOwner
        fields = [
            'shaba',
            *AccountProfileSerializer.Meta.fields,
        ]


class ProfilePictureSerializer(ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = [
            'id',
            'account',
            'file',
            'is_active',
        ]
