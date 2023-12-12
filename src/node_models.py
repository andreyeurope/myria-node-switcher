from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
import croniter
import datetime
import isodate

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class NodeSchedule:
    """Class for keeping track of an item in inventory."""
    cron: str
    runningTime: str

    def get_croniter(self, currentDate) -> croniter:
        return croniter.croniter(self.cron, currentDate)
    
    def get_duration(self) -> datetime.timedelta:
        return isodate.parse_duration(str)

    def should_be_running(self, currentDate: datetime.datetime) -> bool:
        duration = self.get_duration()
        croniter = self.get_croniter(currentDate)
        prevRunStart = croniter.get_prev(currentDate)
        prevRunEnd = prevRunStart + duration
        nextRunStart = croniter.get_next(currentDate)
        nextRunEnd = nextRunStart + duration
        return (currentDate >= nextRunStart and currentDate <= nextRunEnd) or (currentDate >= prevRunStart and currentDate <= prevRunEnd)

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Node:
    """Class for keeping track of an item in inventory."""
    name: str
    apiKey: str
    schedule: NodeSchedule
