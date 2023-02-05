from django.core.exceptions import ValidationError
from django.db import models, transaction

from financial.enums import MANUAL_TRANSACTION_STATES, MANUAL_TRANSACTION_STATE_ACCEPTED, \
    MANUAL_TRANSACTION_STATE_REJECTED, MANUAL_TRANSACTION_STATE_PENDING, MANUAL_TRANSACTION_TYPES, \
    MANUAL_TRANSACTION_TYPE_WITHDRAW_REQUEST, MANUAL_TRANSACTION_TYPE_CHARGE_REQUEST
from financial.transaction_descriptions import MANUAL_TRANSACTION_ACCEPTED
from utility.mixins import StatefulModelMixin
from utility.models import HistoricalBaseModel


class ManualTransaction(StatefulModelMixin, HistoricalBaseModel):
    """
    money aggregates in our business bank account then goes to its owner account.
        + all this exiting from our bank account to our user bank accounts must have one ManualTransaction.
        + all this aggregating in our bank account from our user bank accounts must have one ManualTransaction.
    """

    def init_old_instance_fields(self):
        self._current_state = self.state
        self._amount = self.amount
        self._wallet = self.wallet

    wallet = models.ForeignKey(
        to='financial.wallet',
        on_delete=models.PROTECT,
        related_name='withdraw_requests',
        verbose_name='کیف پول مربوطخ'
    )

    amount = models.PositiveIntegerField(
        verbose_name='مبلغ',
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='توضیحات'
    )

    type = models.CharField(
        max_length=64,
        default=MANUAL_TRANSACTION_TYPE_WITHDRAW_REQUEST,
        choices=MANUAL_TRANSACTION_TYPES,
        verbose_name='نوع',
    )

    # In case some withdraw_requests are created wrong, only accepted state means
    # it is paid and transaction must be created
    state = models.CharField(
        max_length=64,
        default=MANUAL_TRANSACTION_STATE_PENDING,
        choices=MANUAL_TRANSACTION_STATES,
        verbose_name='وضعیت',
    )

    def clean(self):
        if self.is_update:
            if self.is_transition():
                if self.state in [MANUAL_TRANSACTION_STATE_ACCEPTED, MANUAL_TRANSACTION_STATE_REJECTED]:
                    raise ValidationError({
                        'state': ['بعد از رد یا تایید درخواست، نمی‌توان وضعیت آن‌را تغییر داد']
                    })
            if self._amount != self.amount and self.state != MANUAL_TRANSACTION_STATE_PENDING:
                raise ValidationError({
                    'amount': ['بعد از رد یا تایید درخواست، نمی‌توان مقدار آن‌را تغییر داد']
                })
            if self._wallet != self.wallet:
                raise ValidationError({
                    'wallet': ['نمی‌توان کیف پول آن‌را تغییر داد']
                })

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        with transaction.atomic():
            super().save(force_insert, force_update, using, update_fields)
            if self.is_transition() and self.state == MANUAL_TRANSACTION_STATE_ACCEPTED:
                self.settle_manual_transaction()

    def settle_manual_transaction(self):
        from financial.models import Transaction
        return Transaction.objects.create(
            wallet=self.wallet,
            parameters={'withdraw_request_id': self.id},
            amount=self.amount if self.type == MANUAL_TRANSACTION_TYPE_CHARGE_REQUEST else -self.amount,
            description=MANUAL_TRANSACTION_ACCEPTED.value.format(
                manual_transaction_id=self.id,
                manual_transaction_type_fa=self.get_type_display(),
                account_id=self.wallet.account.id,
                account_type=self.wallet.account.get_account_type_display(),
            )
        )

    class Meta:
        verbose_name = 'تراکنش دستی'
        verbose_name_plural = 'تراکنش‌های دستی'
