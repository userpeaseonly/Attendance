from enum import Enum

# create your utils here

class AttendanceStatus(Enum):
    GOOD = 0
    NOT_GOOD = 1
    BAD = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


