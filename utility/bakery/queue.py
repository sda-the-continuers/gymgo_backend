import abc

from django.utils import timezone

from utility.bakery import QueueInterface


class Queue(QueueInterface, abc.ABC):
    sub_queues = []

    @classmethod
    @abc.abstractmethod
    def first(cls):
        pass

    @classmethod
    def count(cls):
        return sum([queue.count() for queue in cls.sub_queues])

    @classmethod
    def latency(cls) -> timezone.timedelta:
        latency = timezone.ZERO
        for queue in cls.sub_queues:
            latency = max(latency, queue.latency())

        return latency

