from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer

from gym.models import ClubSMS, ClubSMSForDiscount
from gym.serializers import ClubDiscountDeserializer


class ClubSMSDeserializer(ModelSerializer):
    message = serializers.CharField(max_length=900)

    def clean(self, instance):
        instance.clean(validation_error_class=ValidationError)

    def create(self, validated_data):
        with transaction.atomic():
            instance: ClubSMS = super().create(validated_data)
            instance.clean(validation_error_class=ValidationError)
            return instance

    class Meta:
        model = ClubSMS
        fields = [
            'club',
            'contacts',
            'message',
        ]


class ClubSMSForDiscountDeserializer(ClubSMSDeserializer):

    def clean(self, instance: ClubSMS):
        super().clean(instance.concrete_instance)

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        try:
            _ = data['discount']
        except KeyError:
            raise ValidationError({'discount': ['این فیلد لازم است']})
        self.fields['discount'] = ClubDiscountDeserializer()

    def to_internal_value(self, data):
        data['discount']['club'] = data['club']
        data['discount']['contacts'] = data['contacts']
        data = super().to_internal_value(data)
        return data

    def create(self, validated_data):
        with transaction.atomic():
            validated_data.pop('discount')
            discount_serializer = ClubDiscountDeserializer(data=self.data['discount'], context=self.context)
            discount_serializer.is_valid(raise_exception=True)
            discount = discount_serializer.save()
            validated_data['discount'] = discount
            return super().create(validated_data)

    class Meta:
        model = ClubSMSForDiscount
        fields = [
            *ClubSMSDeserializer.Meta.fields,
            'discount',
        ]
