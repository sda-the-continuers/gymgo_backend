from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from gym.models import ClubContact


class ClubContactSerializer(ModelSerializer):
    athlete_data = serializers.SerializerMethodField()
    gym_complex = serializers.IntegerField(source='club.gym_complex.id')

    def get_athlete_data(self, instance):
        return {
            'id': instance.athlete_id,
            'reserves_count': instance.reserves_count
        }

    class Meta:
        model = ClubContact
        fields = ['id', 'club', 'gym_complex', 'full_name', 'phone_number', 'athlete_data']
