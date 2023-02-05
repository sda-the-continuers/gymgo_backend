from abc import ABC

from rest_framework.permissions import BasePermission


class BaseGymtimeAccountPermission(BasePermission):

    def get_user(self, request):
        try:
            return request.user
        except:
            return None

    def get_account(self, request) -> 'Account':
        try:
            return self.get_user(request).account
        except:
            return None


class IsAthlete(BaseGymtimeAccountPermission):

    def has_permission(self, request, view):
        if account := self.get_account(request):
            return account.try_athlete is not None


class IsGymOwner(BaseGymtimeAccountPermission):
    def has_permission(self, request, view):
        if account := self.get_account(request):
            return account.try_gym_owner is not None
