from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import JSONField

from financial.enums import TRANSACTION_TYPES, TRANSACTION_TYPE_WITHDRAW, TRANSACTION_TYPE_DEPOSIT
from utility.models import HistoricalBaseModel


class Transaction(HistoricalBaseModel):
    """
    both following types must have one transaction:
        + wallet charging
        - wallet withdrawal
    all of transactions must be created automatically in the app code (or will be a case of abuse)
    """

    def init_old_instance_fields(self):
        self._amount = self.amount
        self._wallet = self.wallet
        self._parameters = self.parameters
        self._description = self.description

    wallet = models.ForeignKey(
        to='financial.Wallet',
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='کیف پول مربوطه',
    )

    amount = models.IntegerField(
        verbose_name='مقدار تراکنش'
    )

    parameters = JSONField(
        verbose_name='پارامترها',
        null=True,
        blank=True,
    )

    description = models.CharField(
        max_length=256,
        verbose_name='توضیحات',
    )

    def clean(self):
        if self.is_update:
            for field in [
                'wallet',
                'amount',
                'parameters',
                'description'
            ]:
                if getattr(self, f'_{field}') != getattr(self, field):
                    raise ValidationError({
                        field: ['فیلد های تراکنش بعد از ساخته شدن نباید تغییر کنند.']
                    })

    @property
    def type(self):
        return TRANSACTION_TYPE_WITHDRAW if self.amount < 0 else TRANSACTION_TYPE_DEPOSIT

    @property
    def type_fa(self):
        return dict(TRANSACTION_TYPES)[self.type]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        with transaction.atomic():
            if self._amount != self.amount:
                self.wallet.total_amount += self.amount
                self.wallet.save()
            super(Transaction, self).save(force_insert, force_update, using, update_fields)
            self.init_old_instance_fields()

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
