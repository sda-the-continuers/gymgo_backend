import typing

from crm.enums import CRM_TASK_TYPE_PAY_OR_PAYBACK_SCHEDULED_SESSION_TO_GYM_OWNER_NAME, \
    CRM_TASK_TYPE_PAYBACK_RESERVATION_TO_ATHLETE_NAME
from crm.models import CRMTaskType
from events import emitter
from financial.event_types import FinancialEventTypes

if typing.TYPE_CHECKING:
    from gym.models import ScheduledSession
    from reservation.models import Reserve
    from financial.models import Transaction


@emitter.on(FinancialEventTypes.SCHEDULED_SESSION_TRANSACTION_CREATED)
def pay_to_gym_owner(scheduled_session: 'ScheduledSession', transaction: 'Transaction'):
    CRMTaskType.create_task(
        CRM_TASK_TYPE_PAY_OR_PAYBACK_SCHEDULED_SESSION_TO_GYM_OWNER_NAME,
        scheduled_session.gymnasium.gym_complex.owner.crm_account,
        scheduled_session=scheduled_session,
        transaction=transaction,
    )


@emitter.on(FinancialEventTypes.RESERVE_TRANSACTION_CREATED)
def payback_to_athlete(reserve: 'Reserve', transaction: 'Transaction'):
    if transaction.amount > 0:
        CRMTaskType.create_task(
            CRM_TASK_TYPE_PAYBACK_RESERVATION_TO_ATHLETE_NAME,
            reserve.athlete.crm_account,
            reserve=reserve,
            transaction=transaction,
        )
