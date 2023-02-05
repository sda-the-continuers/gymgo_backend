from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum
from django.utils import timezone
from jalali_date import datetime2jalali

from events import emitter
from gym.enums import SCHEDULED_SESSION_STATES, SCHEDULED_SESSION_VALID_TRANSITIONS, SCHEDULED_SESSION_STATE_RESERVED, \
    SCHEDULED_SESSION_STATE_AVAILABLE
from gym.event_types import GymEventTypes
from reservation.enums import RESERVE_STATE_CANCELLED
from utility.mixins import StatefulModelMixin
from utility.models import HistoricalBaseModel


class ScheduledSession(StatefulModelMixin, HistoricalBaseModel):

    def init_old_instance_fields(self):
        self._current_state = self.state
        self._price = self.price
        self._gym_owner_price = self.gym_owner_price

    gymnasium = models.ForeignKey(
        to='gym.Gymnasium',
        on_delete=models.CASCADE,
        related_name='scheduled_sessions',
        verbose_name='ورزشگاه مربوطه'
    )

    start_datetime = models.DateTimeField(
        verbose_name='زمان شروع سانس'
    )

    end_datetime = models.DateTimeField(
        verbose_name='زمان پایان سانس'
    )

    state = models.CharField(
        choices=SCHEDULED_SESSION_STATES,
        verbose_name='وضعیت',
        max_length=128,
        default=SCHEDULED_SESSION_STATE_AVAILABLE,
    )

    price = models.PositiveIntegerField(
        verbose_name='مبلغ'
    )

    gym_owner_price = models.PositiveIntegerField(
        verbose_name='مبلغ پرداختی به صاحب ورزشگاه'
    )

    valid_transitions_map = SCHEDULED_SESSION_VALID_TRANSITIONS

    @property
    def jalali_start_datetime(self):
        return datetime2jalali(self.start_datetime)

    @property
    def jalali_end_datetime(self):
        return datetime2jalali(self.end_datetime)

    @property
    def active_reserve(self):
        from reservation.models import Reserve
        return Reserve.objects.filter(scheduled_session_id=self.id).exclude(state=RESERVE_STATE_CANCELLED).first()

    def can_be_reserved(self):
        return (
                self.is_state_transition_valid(SCHEDULED_SESSION_STATE_RESERVED)
                and
                self.start_datetime >= timezone.now()
        )

    @property
    def transactions(self):
        from financial.models.transaction import Transaction
        return Transaction.objects.filter(
            wallet_id=self.gymnasium.gym_complex.owner.wallet_id,
            parameters=dict(scheduled_session_id=self.id),
        )

    @property
    def paid_price_to_gym_owner(self):
        return self.transactions.aggregate(total_amount=Sum('amount')).get('total_amount') or 0

    def clean(self, validation_error_class=ValidationError):
        self.validate_state_transition(validation_error_class)
        if self.state == SCHEDULED_SESSION_STATE_RESERVED:
            if not self.active_reserve:
                raise validation_error_class({
                    'state': ['یک {} در وضعیت {} باید حتما دارای رزرو غیر کنسل باشد.'.format(
                        self.meta.verbose_name,
                        self.get_state_display()
                    )]
                })
        if self.start_datetime > self.end_datetime:
            raise validation_error_class({
                'start_datetime': [
                    'این فیلد باید قبل تر از فیلد {} باشد.'.format(
                        self.get_field('end_datetime').verbose_name
                    )
                ]
            })
        if self.is_update:
            if (
                    self._price != self.price or self._gym_owner_price != self.gym_owner_price
            ) and self.state == SCHEDULED_SESSION_STATE_RESERVED:
                changed_field = 'price' if self._price != self.price else 'gym_owner_price'
                raise validation_error_class({
                    changed_field: [
                        'این فیلد نمی‌تواند در استیت {} تغییر کند.'.format(
                            self.get_state_display()
                        )
                    ]
                })

    def before_create(self):
        price = self.price or self.gymnasium.price
        gym_owner_price = self.gym_owner_price or self.gymnasium.gym_owner_price
        if price is None or gym_owner_price is None:
            raise ValueError('please insert both <price> and <gym_owner_price>')
        self.price, self.gym_owner_price = price, gym_owner_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        with transaction.atomic():
            super().save(force_insert, force_update, using, update_fields)
            self.check_changes_and_emit_events()
            self.init_old_instance_fields()

    def check_changes_and_emit_events(self):
        if self._current_state != self.state:
            emitter.emit(GymEventTypes.SCHEDULED_SESSION_STATE_CHANGED, self)

    class Meta:
        verbose_name = 'سانس ورزشگاه'
        verbose_name_plural = 'سانس‌های ورزشگاه'
