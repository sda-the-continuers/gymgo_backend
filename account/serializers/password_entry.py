from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.status import HTTP_401_UNAUTHORIZED

from account.models import GymOwner


class GymOwnerPasswordLoginSerializer(Serializer):
    phone_number = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        phone_number, password = attrs['phone_number'], attrs['password']
        gym_owner_user = get_object_or_404(
            get_user_model().objects.all(),
            username=GymOwner.construct_user_key(phone_number)
        )

        if not check_password(password, gym_owner_user.password):
            raise ValidationError(
                {'password': 'رمز عبور اشتباه است'},
                code=HTTP_401_UNAUTHORIZED
            )

        return attrs


class GymOwnerChangePasswordSerializer(ModelSerializer):
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance

    def validate_old_password(self, old_password):
        gym_owner_user = self.context['request'].user
        if not check_password(old_password, gym_owner_user.password):
            raise ValidationError(
                {'password': 'رمز عبور سابق خود را اشتباه وارد کردید'},
                code=HTTP_401_UNAUTHORIZED
            )
        return old_password

    def validate(self, attrs):
        attrs.pop('old_password')
        attrs['password'] = attrs.pop('new_password')
        return attrs

    class Meta:
        model = get_user_model()
        fields = [
            'old_password',
            'new_password',
        ]


class GymOwnerSetPasswordSerializer(Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True)

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance

    def validate(self, attrs):
        user = self.context['request'].user
        if user.password:
            raise ValidationError({
                'password': 'قبلا پسورد وارد شده است'
            })

        attrs['password'] = attrs.pop('new_password')
        return attrs

    class Meta:
        model = get_user_model()
        fields = [
            'new_password',
        ]