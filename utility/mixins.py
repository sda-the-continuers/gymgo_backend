from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer


class StatefulModelMixin:
    valid_transitions_map = None

    def is_transition(self) -> bool:
        return self._current_state != self.state

    def is_transiting(self, current_state, new_state) -> bool:
        return (self._current_state, self.state) == (current_state, new_state)

    def is_transiting_to(self, new_state) -> bool:
        return self.is_transition() and self.state == new_state

    def is_state_transition_valid(self, new_state) -> bool:
        return new_state in self.valid_transitions_map[self._current_state]

    def validate_state_transition(self, validation_error_class):
        if self.is_transition():
            if not self.is_state_transition_valid(self.state):
                raise validation_error_class({
                    'state': ['این {} در وضعیت درستی برای تغییر وضعیت مطلوب شما قرار ندارد.'.format(
                        self.meta.verbose_name
                    )]
                })


class PhoneNumberSerializer(Serializer):
    phone_number = serializers.CharField(max_length=16)

    @staticmethod
    def correct_phone_number_format(phone_number):
        return phone_number.isnumeric() and len(phone_number) == 11 and phone_number.startswith('09')

    def validate_phone_number(self, phone_number):
        if not self.correct_phone_number_format(phone_number):
            raise ValidationError('شماره ورودی فرمت اشتباهی دارد')

        return phone_number
