import abc


class QueueInterface(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def first(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def count(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def latency(cls):
        pass

    @classmethod
    def __len__(cls):
        return cls.count()
