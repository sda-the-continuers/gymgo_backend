from rest_framework.serializers import ModelSerializer

from account.models import Athlete
from gym.models import SportType, SportTypeIcon


class SportTypeIconSerializer(ModelSerializer):
    class Meta:
        model = SportTypeIcon
        fields = ['id', 'sport_type', 'file']


class FavoriteSportsSerializer(ModelSerializer):
    icon = SportTypeIconSerializer()

    class Meta:
        model = SportType
        fields = ['id', 'title', 'title_fa', 'icon']


class SelectFavoriteSportsSerializer(ModelSerializer):
    class Meta:
        model = Athlete
        fields = ['id', 'favorite_sports']
