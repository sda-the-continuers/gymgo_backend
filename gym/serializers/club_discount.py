from discount.serializer import DiscountDeserializer
from gym.models import ClubDiscount


class ClubDiscountDeserializer(DiscountDeserializer):

    class Meta:
        model = ClubDiscount
        fields = [
            *DiscountDeserializer.Meta.fields,
            'club',
            'contacts',
        ]
