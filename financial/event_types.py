from enum import Enum

from events.event_types import unique_event_types


@unique_event_types
class FinancialEventTypes(Enum):
    SCHEDULED_SESSION_TRANSACTION_CREATED = 0
    RESERVE_TRANSACTION_CREATED = 1
