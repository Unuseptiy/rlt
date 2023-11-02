import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class GroupType(Enum):
    hour: str = "hour"
    day: str = "day"
    month: str = "month"


class Request(BaseModel):
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: GroupType

    @field_validator("dt_upto")
    def is_valid_time_interval(cls, v, values):
        if not v >= values.data.get("dt_from"):
            raise ValueError("Невалидный временной интервал")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "dt_from": "2022-09-01T00:00:00",
                "dt_upto": "2022-12-31T23:59:00",
                "group_type": "month",
            }
        }
