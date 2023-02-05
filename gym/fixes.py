import json

from django.db import transaction

from gym.models import GymnasiumAttribute


def create_gymnasium_attributes():
    with open('gym/resources/gymnasium_attributes.json', mode='r') as f:
        attributes = json.load(f)
        with transaction.atomic():
            for attr in attributes:
                GymnasiumAttribute.objects.get_or_create(**attr)
