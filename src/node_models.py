from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from croniter import croniter
from isodate import parse_duration
from datetime import datetime, timedelta
import logging

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class NodeSchedule:
    cron: str
    runningTime: str
    
    def get_duration(self) -> timedelta:
        return parse_duration(self.runningTime)

    def should_be_running(self, currentDate: datetime) -> bool:
        duration = self.get_duration()
        iter = croniter(self.cron, currentDate)
        prevRunStart = iter.get_prev(datetime)
        prevRunEnd = prevRunStart + duration
        nextRunStart = iter.get_next(datetime)
        nextRunEnd = nextRunStart + duration

        return nextRunStart <= currentDate <= nextRunEnd or prevRunStart <= currentDate <= prevRunEnd

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Node:
    name: str
    apiKey: str
    schedule: NodeSchedule

    def should_be_running(self, currentDate: datetime) -> bool:
        return self.schedule.should_be_running(currentDate)
