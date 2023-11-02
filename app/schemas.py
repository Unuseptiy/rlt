import datetime

from enum import Enum
from pydantic import BaseModel


class GroupType(Enum):
    hour: str = "hour"
    day: str = "day"
    month: str = "month"


class Request(BaseModel):
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: GroupType

    class Config:
        json_schema_extra = {
            "example": {
                "dt_from": "2022-09-01T00:00:00",
                "dt_upto": "2022-12-31T23:59:00",
                "group_type": "month"
            }
        }
