from enum import Enum, unique

all_event_types = set()


def unique_event_types(enumeration):
    unique(enumeration)
    for name in enumeration.__members__.keys():
        if name in all_event_types:
            raise ValueError(f'duplicate event type {name}')
        all_event_types.add(name)
    return enumeration


@unique_event_types
class EventTypes(Enum): pass
