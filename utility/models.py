from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import QuerySet
from jalali_date import datetime2jalali
from simple_history.models import HistoricalRecords


def filter_active_objects(queryset) -> QuerySet:
    return queryset.filter(is_deleted=False)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return filter_active_objects(super().get_queryset())


class CreateHistoryModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    @property
    def jalali_created(self):
        return datetime2jalali(self.created)

    def get_jalali_created(self):
        return self.jalali_created.strftime('%H:%M - %y/%m/%d')

    get_jalali_created.short_description = 'تاریخ ایجاد'

    class Meta:
        abstract = True


class UpdateHistoryModel(models.Model):
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )

    @property
    def jalali_updated(self):
        return datetime2jalali(self.updated)

    def get_jalali_updated(self):
        return self.jalali_updated.strftime('%H:%M - %y/%m/%d')

    get_jalali_updated.short_description = 'تاریخ بروزرسانی'

    class Meta:
        abstract = True


class BaseHistoryModel(CreateHistoryModel, UpdateHistoryModel):
    class Meta:
        abstract = True


class BaseModel(BaseHistoryModel):
    all_objects = models.Manager()
    objects = ActiveManager()

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='آیا حذف شده است؟',
        db_index=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_old_instance_fields()

    def init_old_instance_fields(self):
        """
            Initialize every field needed from old instance in here.
            These fields will be rewritten on __init__ and refresh_from_db.
        """
        pass

    def refresh_from_db(self, using=None, fields=None):
        super().refresh_from_db(using=using, fields=fields)
        self.init_old_instance_fields()

    @property
    def meta(self):
        return self._meta

    @property
    def is_create(self):
        return not self.pk

    @property
    def is_update(self):
        return not self.is_create

    @property
    def old_instance(self):
        return self.__class__.objects.filter(pk=self.pk).first()

    class Meta:
        abstract = True

    def after_create(self):
        """
            on_create is a simple callback function called after creating
            a new record on database. (for first time)
            this function is in a same transaction with save function
        """
        pass

    def before_create(self):
        """
            before_create is a simple callback function called before creating
            a new record on database. (for first time)
            this function is in a same transaction with save function
        """
        pass

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        with transaction.atomic():
            is_create = bool(self.is_create)
            if is_create:
                self.before_create()
            super().save(force_insert, force_update, using, update_fields)
            if is_create:
                self.after_create()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)

    @classmethod
    def get_field(cls, field):
        return cls._meta.get_field(field)


class HistoricalBaseModel(BaseModel):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class BaseLocationModel(models.Model):
    long = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='عرض جغرافیایی',
        null=True,
        blank=True,
    )

    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='طول جغرافیایی',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class EnumBaseModel(models.Model):

    title = models.CharField(
        max_length=256,
        verbose_name='عنوان',
        unique=True,
    )

    title_fa = models.CharField(
        max_length=256,
        verbose_name='عنوان فارسی',
        unique=True,
    )

    def __str__(self):
        return f'{self.id}: {self.title_fa}'

    class Meta:
        abstract = True


class PositiveFloatField(models.FloatField):
    default_validators = [MinValueValidator(0)]

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            **kwargs,
        })


class PercentageField(PositiveFloatField):
    default_validators = [*PositiveFloatField.default_validators, MinValueValidator(100)]

    def formfield(self, **kwargs):
        return super().formfield(**{
            'max_value': 100,
            **kwargs,
        })

