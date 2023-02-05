from typing import TYPE_CHECKING

from events import emitter
from gym.enums import SCHEDULED_SESSION_STATE_RESERVED, SCHEDULED_SESSION_STATE_AVAILABLE, \
    SCHEDULED_SESSION_STATE_CANCELLED
from gym.models import ScheduledSession
from reservation.enums import RESERVE_STATE_PURCHASED, RESERVE_STATE_CANCELLED, RESERVE_STATE_DONE
from reservation.event_types import ReservationEventTypes

if TYPE_CHECKING:
    from reservation.models import Reserve


@emitter.on(ReservationEventTypes.RESERVE_STATE_CHANGED)
def handle_reserve_state_changed(reserve: 'Reserve'):
    ss: ScheduledSession = reserve.scheduled_session
    ss_state = None
    if reserve.is_transiting_to(RESERVE_STATE_PURCHASED):
        ss_state = SCHEDULED_SESSION_STATE_RESERVED
    elif reserve.is_transiting(RESERVE_STATE_PURCHASED, RESERVE_STATE_CANCELLED):
        ss_state = SCHEDULED_SESSION_STATE_AVAILABLE
    elif reserve.is_transiting(RESERVE_STATE_DONE, RESERVE_STATE_CANCELLED):
        """
        If reserve was done it meant that the time of scheduled session was passed.
        so if it gets cancelled the scheduled session can't be reserved from others anymore.
        """
        ss_state = SCHEDULED_SESSION_STATE_CANCELLED
    if ss_state:
        ss.state = ss_state
        ss.clean()
        ss.save()
