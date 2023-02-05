from utility.bakery import Queue


class PriorityQueue(Queue):
    sub_queues = []

    @classmethod
    def first(cls):
        for queue in cls.sub_queues:
            if queue.count() > 0:
                return queue.first()
        return None
