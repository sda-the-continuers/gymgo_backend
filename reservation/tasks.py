import logging

from celery import shared_task
from django.core.exceptions import ValidationError
from django.utils import timezone

from reservation.enums import RESERVE_STATE_PURCHASED, RESERVE_STATE_DONE
from reservation.models import Reserve

logger = logging.getLogger(__name__)


@shared_task(queue='gym')
def make_reserves_done():
    for reserve in list(
        Reserve.objects.filter(
            state=RESERVE_STATE_PURCHASED,
            scheduled_session__end_datetime__lte=timezone.now(),
        ).order_by(
            'scheduled_session__end_datetime',
        )
    ):
        try:
            reserve.state = RESERVE_STATE_DONE
            reserve.clean()
            reserve.save()
        except (ValueError, ValidationError) as e:
            logger.error(
                f'Failed make reserve with id {reserve.id} DONE.',
                exc_info=True, extra={'exception': e, 'reserve': reserve}
            )
