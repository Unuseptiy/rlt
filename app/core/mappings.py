import datetime

from dateutil.relativedelta import relativedelta

group_type__pattern = {
    "hour": "%Y-%m-%dT%H",
    "day": "%Y-%m-%d",
    "month": "%Y-%m",
}

group_type__delta = {
    "hour": datetime.timedelta(hours=1),
    "day": datetime.timedelta(days=1),
    "month": relativedelta(months=1),
}
