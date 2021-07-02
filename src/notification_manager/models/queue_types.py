from enum import Enum


class QueueType(Enum):
    NEWOFFERING = 'offering.new'

    @classmethod
    def is_valid(cls, name):
        return name in cls._value2member_map_
