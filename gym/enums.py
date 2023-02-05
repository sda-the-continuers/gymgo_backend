SCHEDULED_SESSION_STATE_AVAILABLE = 'AVAILABLE'
SCHEDULED_SESSION_STATE_PENDING = 'PENDING'
SCHEDULED_SESSION_STATE_RESERVED = 'RESERVED'
SCHEDULED_SESSION_STATE_CANCELLED = 'CANCELLED'


SCHEDULED_SESSION_STATES = (
    (SCHEDULED_SESSION_STATE_AVAILABLE, 'دردسترس'),
    (SCHEDULED_SESSION_STATE_PENDING, 'در حال انتظار'),
    (SCHEDULED_SESSION_STATE_RESERVED, 'رزرو شده'),
    (SCHEDULED_SESSION_STATE_CANCELLED, 'کنسل شده'),
)

SCHEDULED_SESSION_VALID_TRANSITIONS = {
    SCHEDULED_SESSION_STATE_AVAILABLE: [
        SCHEDULED_SESSION_STATE_PENDING,
        SCHEDULED_SESSION_STATE_RESERVED,
        SCHEDULED_SESSION_STATE_CANCELLED,
    ],
    SCHEDULED_SESSION_STATE_PENDING: [
        SCHEDULED_SESSION_STATE_AVAILABLE,
        SCHEDULED_SESSION_STATE_RESERVED,
    ],
    SCHEDULED_SESSION_STATE_RESERVED: [
        SCHEDULED_SESSION_STATE_CANCELLED
    ],
    SCHEDULED_SESSION_STATE_CANCELLED: []
}

GYM_USAGE_EQUIPMENT_TYPE_BALL = 'BALL'
GYM_USAGE_EQUIPMENT_TYPES = (
    (GYM_USAGE_EQUIPMENT_TYPE_BALL, 'توپ'),
)