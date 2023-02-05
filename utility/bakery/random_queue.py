import random

from utility.bakery import Queue


class RandomQueue(Queue):
    weights = []

    @classmethod
    def first(cls):
        if cls.count() == 0:
            return None

        valid_queues = []
        valid_queue_weights = []
        for i, queue in enumerate(cls.sub_queues):
            if queue.count() > 0:
                valid_queues.append(queue)
                valid_queue_weights.append(cls.weights[i])

        return random.choices(valid_queues, valid_queue_weights)[0].first()
