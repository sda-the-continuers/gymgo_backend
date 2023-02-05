from celery import shared_task
from django.db import transaction
from django.utils import timezone

from sms.enums import GYMTIME_SMS_AWAITING_SENDING, GYMTIME_SEND_SMS_MINIMUM_DELAY_MINUTES
from sms.models import GymtimeSimpleSMS
from utility.bakery import QuerysetQueue


class GymtimeMessagesQueue(QuerysetQueue):

    @classmethod
    def get_queryset(cls):
        return GymtimeSimpleSMS.objects.filter(
            state=GYMTIME_SMS_AWAITING_SENDING, created__lte=timezone.now() - timezone.timedelta(
                minutes=GYMTIME_SEND_SMS_MINIMUM_DELAY_MINUTES
            )
        )


@shared_task(queue='sms')
def send_gymtime_messages():
    for _ in range(5):
        with transaction.atomic():
            sms: GymtimeSimpleSMS = GymtimeMessagesQueue.get_locked_first()
            sms = sms.concrete_instance
            sms.validate_and_send(save=True)
