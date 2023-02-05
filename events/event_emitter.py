import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class EventEmitter(object):

    # this class must be used as singleton

    def __init__(self):
        self._handlers = defaultdict(list)

    def emit(self, event_type, obj, *args, **kwargs):
        for func in self._handlers[event_type]:
            try:
                func(obj, *args, **kwargs)
            except Exception as e:
                logger.error('Could not emit event event_type: {}'.format(event_type.name), e, exc_info=True)

    def on(self, event_type):
        def decorator(fn):
            assert not hasattr(fn, '__is_registered_on_events__'), "function has been registered before."
            fn.__is_registered_on_events__ = True
            self._handlers[event_type].append(fn)
            return fn
        return decorator


emitter = EventEmitter()
