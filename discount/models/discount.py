from itertools import chain
from typing import Iterable, TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet

from discount.utils import DiscountApplierComponent
from utility.models import HistoricalBaseModel

if TYPE_CHECKING:
    from discount.models import DiscountRestriction


class Discount(HistoricalBaseModel):
    code = models.CharField(
        max_length=32,
        verbose_name='کد تخفیف',
    )

    pricing_type = models.OneToOneField(
        to='discount.DiscountPricingType',
        related_name='discount',
        on_delete=models.PROTECT,
        verbose_name='نحوه قیمت‌گذاری',
    )

    def get_discount_amount(self, price):
        return self.pricing_type.concrete_instance.get_discount_amount(price)

    @property
    def try_advertiser_discount(self):
        from account.models import AthleteDiscount
        if isinstance(self, AthleteDiscount):
            return self
        try:
            return self.athletediscount
        except:
            return None

    @property
    def try_club_discount(self):
        from gym.models import ClubDiscount
        if isinstance(self, ClubDiscount):
            return self
        try:
            return self.clubdiscount
        except:
            return None

    @property
    def concrete_instance(self):
        return self.try_club_discount or self.try_advertiser_discount or self

    @property
    def restrictions(self) -> Iterable['DiscountRestriction']:
        from discount.models import DiscountRestriction
        return chain(
            *(
                sub_cls.objects.filter(discount=self)
                for sub_cls in DiscountRestriction.__subclasses__()
            )
        )

    def can_apply_to(self, component: DiscountApplierComponent, raise_exception=False):
        errors = []
        for restriction in self.restrictions:
            try:
                if not restriction.can_apply_to(component, raise_exception=raise_exception):
                    return False
            except ValidationError as e:
                errors.append(e)
        if not errors:
            return True
        elif not raise_exception:
            return False
        else:
            raise ValidationError(errors)

    def can_apply_athlete(self, athlete) -> bool:
        return True

    def get_info(self) -> str:
        return ' '.join([restriction.get_info() for restriction in self.restrictions])

    def __str__(self):
        return 'تخفیف {}: {}'.format(
            self.id,
            self.get_info(),
        )

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف‌ها'


class AthleteBasedDiscount(Discount):

    def can_apply_to(self, component: 'DiscountApplierComponent', raise_exception=False):
        if not self.can_apply_athlete(component.athlete):
            if raise_exception:
                #  just raise this to avoid giving extra information about discount
                raise ValidationError('این کد تخفیف متعلق به شما نیست.')
            return False
        return super().can_apply_to(component, raise_exception=raise_exception)

    def can_apply_athlete(self, athlete) -> bool:
        raise self.athletes_that_can_apply.filter(id=athlete.id).exists()

    @property
    def athletes_that_can_apply(self) -> QuerySet:
        raise NotImplementedError

    class Meta:
        abstract = True
