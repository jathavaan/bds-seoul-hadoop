from enum import Enum


class ProcessType(Enum):
    CACHE_CHECK = "cache_check"
    SCRAPE = "scrape"
    MAPREDUCE = "mapreduce"
    CACHE_RESULT = "cache_result"

    @classmethod
    def from_string(cls, value: str) -> "ProcessType":
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid ProcessType: {value}")


class ProcessStatus(Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    SKIPPED = "skipped"
    COMPLETED = "completed"
    FAILED = "failed"

    @classmethod
    def from_string(cls, value: str) -> "ProcessStatus":
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid ProcessStatus: {value}")
