from enum import Enum

from events.event_types import unique_event_types


@unique_event_types
class ReservationEventTypes(Enum):
    RESERVE_STATE_CHANGED = 0
