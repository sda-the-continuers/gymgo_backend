import typing
from typing import Tuple

from rest_framework_simplejwt.tokens import RefreshToken

if typing.TYPE_CHECKING:
    from account.models import Account


def get_jwt_token(account: 'Account') -> Tuple[str, str]:
    account = account.concrete_instance
    token = RefreshToken.for_user(account.user)
    for claim_key, claim_val in account.get_jwt_claims().items():
        token[claim_key] = claim_val
    refresh, access = str(token), str(token.access_token)
    return refresh, access
