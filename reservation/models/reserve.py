from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum

from events import emitter
from reservation.enums import RESERVE_STATES, RESERVE_STATE_PURCHASED, RESERVE_VALID_TRANSITIONS
from reservation.event_types import ReservationEventTypes
from utility.mixins import StatefulModelMixin
from utility.models import HistoricalBaseModel


class Reserve(StatefulModelMixin, HistoricalBaseModel):

    def init_old_instance_fields(self):
        self._current_state = self.state

    scheduled_session = models.ForeignKey(
        to='gym.ScheduledSession',
        on_delete=models.CASCADE,
        related_name='reserves',
        verbose_name='سانس مربوطه',
    )

    gym_usage = models.ForeignKey(
        to='gym.GymUsage',
        on_delete=models.CASCADE,
        related_name='reserves',
        verbose_name='کاربری ورزشگاه مربوطه',
    )

    athlete = models.ForeignKey(
        to='account.Athlete',
        on_delete=models.CASCADE,
        related_name='reserves',
        verbose_name='ورزشکار',
    )

    state = models.CharField(
        choices=RESERVE_STATES,
        verbose_name='وضعیت',
        max_length=128,
        default=RESERVE_STATE_PURCHASED,
    )

    valid_transitions_map = RESERVE_VALID_TRANSITIONS

    discount = models.ForeignKey(
        to='discount.Discount',
        on_delete=models.PROTECT,
        related_name='reserves',
        verbose_name='تخفیف',
        null=True, blank=True
    )
    
    @property
    def transactions(self):
        from financial.models.transaction import Transaction
        return Transaction.objects.filter(
            wallet_id=self.athlete.wallet_id,
            parameters=dict(reserve_id=self.id),
        )
    
    @property
    def paid_price_from_athlete(self):
        return (self.transactions.aggregate(
            total_amount=Sum('amount')
        ).get('total_amount') or 0) * -1

    def clean(self, validation_error_class=ValidationError):
        self.validate_state_transition(validation_error_class)

    def before_create(self):
        if not self.scheduled_session.can_be_reserved():
            raise ValueError('این {} رزرو دریافت نمی‌کند.'.format(self.scheduled_session.meta.verbose_name))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        with transaction.atomic():
            super().save(force_insert, force_update, using, update_fields)
            self.check_changes_and_emit_events()
            self.init_old_instance_fields()

    def check_changes_and_emit_events(self):
        if self._current_state != self.state:
            emitter.emit(ReservationEventTypes.RESERVE_STATE_CHANGED, self)

    class Meta:
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزروها'

