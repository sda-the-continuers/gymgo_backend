import typing

from events import emitter
from financial.event_types import FinancialEventTypes
from financial.models.transaction import Transaction
from financial.transaction_descriptions import PAY_SCHEDULED_SESSION_TRANSACTION_DESCRIPTION, \
    PAYBACK_RESERVE_TRANSACTION_DESCRIPTION
from gym.enums import SCHEDULED_SESSION_STATE_RESERVED, SCHEDULED_SESSION_STATE_CANCELLED
from gym.event_types import GymEventTypes
from reservation.enums import RESERVE_STATE_CANCELLED
from reservation.event_types import ReservationEventTypes
from utility.text_processing import camel_to_snake

if typing.TYPE_CHECKING:
    from gym.models import ScheduledSession
    from reservation.models import Reserve
    from account.models import Account


def _create_transaction_if_needed(account: 'Account', related_obj, amount, description):
    if amount:
        return Transaction.objects.create(
            wallet=account.wallet,
            parameters={f'{camel_to_snake(related_obj.__class__.__name__)}_id': related_obj.id},
            amount=amount,
            description=description
        )


def pay_or_payback_scheduled_session_to_gym_owner(scheduled_session: 'ScheduledSession', amount: int):
    owner = scheduled_session.gymnasium.gym_complex.owner
    transaction = _create_transaction_if_needed(
        owner, scheduled_session, amount, PAY_SCHEDULED_SESSION_TRANSACTION_DESCRIPTION.format(
            gym_owner_id=owner.id,
            scheduled_session_id=scheduled_session.id,
        )
    )
    if transaction:
        emitter.emit(FinancialEventTypes.SCHEDULED_SESSION_TRANSACTION_CREATED, scheduled_session, transaction)
    return transaction


def pay_scheduled_session_to_gym_owner(scheduled_session: 'ScheduledSession'):
    return pay_or_payback_scheduled_session_to_gym_owner(
        scheduled_session,
        scheduled_session.gym_owner_price - scheduled_session.paid_price_to_gym_owner
    )


def payback_scheduled_session_from_gym_owner(scheduled_session: 'ScheduledSession'):
    return pay_or_payback_scheduled_session_to_gym_owner(
        scheduled_session,
        -scheduled_session.paid_price_to_gym_owner
    )


def payback_reservation_to_athlete(reserve: 'Reserve'):
    athlete = reserve.athlete
    delta_amount = reserve.paid_price_from_athlete
    transaction = _create_transaction_if_needed(
        athlete, reserve, delta_amount, PAYBACK_RESERVE_TRANSACTION_DESCRIPTION.format(
            reserve_id=reserve.id,
            athlete_id=athlete.id,
        )
    )
    if transaction:
        emitter.emit(FinancialEventTypes.RESERVE_TRANSACTION_CREATED, reserve, transaction)
    return transaction


@emitter.on(GymEventTypes.SCHEDULED_SESSION_STATE_CHANGED)
def handle_scheduled_session_state_changed(scheduled_session: 'ScheduledSession'):
    if scheduled_session.state == SCHEDULED_SESSION_STATE_RESERVED:
        pay_scheduled_session_to_gym_owner(scheduled_session)
    elif scheduled_session.is_transiting(SCHEDULED_SESSION_STATE_RESERVED, SCHEDULED_SESSION_STATE_CANCELLED):
        payback_scheduled_session_from_gym_owner(scheduled_session)
        payback_reservation_to_athlete(scheduled_session.active_reserve)


@emitter.on(ReservationEventTypes.RESERVE_STATE_CHANGED)
def handle_reserve_state_changed(reserve: 'Reserve'):
    if reserve.is_transiting_to(RESERVE_STATE_CANCELLED):
        payback_scheduled_session_from_gym_owner(reserve.scheduled_session)
        payback_reservation_to_athlete(reserve)
