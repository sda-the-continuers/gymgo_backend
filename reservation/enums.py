RESERVE_STATE_CREATED = 'CREATED'
RESERVE_STATE_PURCHASED = 'PURCHASED'
RESERVE_STATE_DONE = 'DONE'
RESERVE_STATE_CANCELLED = 'CANCELLED'
RESERVE_STATES = (
    (RESERVE_STATE_CREATED, 'ساخته شده'),
    (RESERVE_STATE_PURCHASED, 'پرداخت شده'),
    (RESERVE_STATE_DONE, 'انجام شده'),
    (RESERVE_STATE_CANCELLED, 'کنسل شده'),
)

RESERVE_VALID_TRANSITIONS = {
    RESERVE_STATE_CREATED: [RESERVE_STATE_PURCHASED,],
    RESERVE_STATE_PURCHASED: [RESERVE_STATE_DONE, RESERVE_STATE_CANCELLED],
    # Reserves get DONE automatically.
    # So there is a change the athlete did not really go to gymnasium for some reasons,
    # then we have to cancel the reservation.
    # This case must not occur often.
    RESERVE_STATE_DONE: [RESERVE_STATE_CANCELLED],
    RESERVE_STATE_CANCELLED: []
}
