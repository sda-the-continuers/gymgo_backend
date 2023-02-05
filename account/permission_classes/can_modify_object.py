from typing import Union

from rest_framework.permissions import SAFE_METHODS, BasePermission

from account.models import Athlete, GymOwner


class CanModifyObject(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return CanModifyRelated(request, obj).is_permitted()


class CanModifyRelated:

    def __new__(cls, request, obj, *args, **kwargs):
        if hasattr(request, 'user'):
            user = request.user
            if hasattr(user, 'account'):
                from account.models import Athlete, GymOwner
                concrete_account = user.account.concrete_instance
                if isinstance(concrete_account, Athlete):
                    return super().__new__(AthleteCanModifyRelated)
                elif isinstance(concrete_account, GymOwner):
                    return super().__new__(GymOwnerCanModifyRelated)

        class _CanNotModifyRelated(CanModifyRelated):

            def is_permitted(self) -> bool:
                return False

        return super().__new__(_CanNotModifyRelated)

    def __init__(self, request, obj):
        self.request = request
        self.obj = obj

    def is_permitted(self) -> bool:
        raise NotImplementedError


class AccountCanModifyRelated(CanModifyRelated):
    related_model_to_account = {}

    def get_related_model_to_account(self):
        return self.related_model_to_account

    def get_permitted_from_object(self):
        _obj = self.obj
        related_model_to_account = self.get_related_model_to_account()
        while _obj is not None and (
                field_names := related_model_to_account.get(_obj.__class__.__name__)
        ) is not None:
            try:
                for field_name in field_names.split('.'):
                    _obj = getattr(_obj, field_name)
            except:
                _obj = None
        return _obj

    @property
    def account(self) -> Union[Athlete, GymOwner]:
        return self.request.user.account.concrete_instance

    def is_permitted(self) -> bool:
        return self.get_permitted_from_object() == self.account


class AthleteCanModifyRelated(AccountCanModifyRelated):
    related_model_to_account = {
        'Reserve': 'athlete',
        'Comment': 'reserve',
        'UsedEquipment': 'reserve',
    }


class GymOwnerCanModifyRelated(AccountCanModifyRelated):
    related_model_to_account = {
        'GymComplex': 'owner',
        'Gymnasium': 'gym_complex',
        'GymUsage': 'gymnasium',
        'ScheduledSession': 'gymnasium',
        'GymUsageEquipment': 'gym_usage',
        'GymContentMedia': 'attachments_interface.concrete_gym',
        'GymThumbnail': 'attachments_interface.concrete_gym',
        'ClubContact': 'gym_complex',
    }
