from django.db import transaction

from rest_framework.serializers import ModelSerializer

from gym.models import GymComplex
from gym.models.gym_complex_nickname import GymComplexNickname
from gym.serializers import GymnasiumCreateSerializer
from gym.serializers.mixins import ThumbnailContentMediaDeserializerMixin
from utility.drf.serializers import CreateForRelatedMixin


class NicknameCreateInGymComplexSerializer(ModelSerializer):
    class Meta:
        model = GymComplexNickname
        fields = [
            'nickname',
        ]


class GymComplexCreateSerializer(CreateForRelatedMixin, ThumbnailContentMediaDeserializerMixin, ModelSerializer):
    gymnasiums = GymnasiumCreateSerializer(many=True)
    nicknames = NicknameCreateInGymComplexSerializer(many=True, required=False)

    def create_for_related(self, gym_complex, serializer_class, data):
        return super().create_for_related(
            'gym_complex', gym_complex, serializer_class, data
        )

    def create(self, validated_data):
        with transaction.atomic():
            gymnasiums_data = validated_data.pop('gymnasiums')
            nicknames_data = validated_data.pop('nicknames', [])
            media_data = validated_data.pop('set_media', [])
            thumbnail_data = validated_data.pop('set_thumbnail', None)

            gym_complex: GymComplex = super().create(validated_data)
            self.create_for_related(gym_complex, GymnasiumCreateSerializer, gymnasiums_data)
            self.create_for_related(gym_complex, NicknameCreateInGymComplexSerializer, nicknames_data)
            from gym.models import GymContentMedia, GymThumbnail
            GymContentMedia.objects.filter(id__in=media_data).update(
                attachments_interface=gym_complex.attachments_interface_id
            )
            GymThumbnail.objects.filter(id=thumbnail_data).update(
                attachments_interface=gym_complex.attachments_interface_id
            )
            return gym_complex

    class Meta:
        model = GymComplex
        fields = [
            'id',
            'phone_number',
            'name',
            'owner',
            'address',
            'description',
            'rules',
            'instagram_username',
            'gymnasiums',
            'nicknames',
            *ThumbnailContentMediaDeserializerMixin.Meta.fields,
        ]
