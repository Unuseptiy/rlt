import datetime
from collections.abc import Coroutine, AsyncIterable

from app.core import mappings
from app.schemas import GroupType


async def prepare_result(
    results: AsyncIterable,
    dt_from: datetime.datetime,
    dt_upto: datetime.datetime,
    group_type: GroupType,
) -> Coroutine[None, None, dict[str, list]]:
    """
    Prepare result from mongo answer.
    :param results: mongo answer
    :type results: AsyncIterable
    :type dt_from: datetime.datetime
    :param dt_upto: end aggregation datetime
    :type dt_upto: datetime.datetime
    :param group_type: aggregation type
    :type group_type: GroupType

    :return: prepared result
    :rtype: Coroutine[None, None, dict[str, list]]
    """
    output = {"dataset": [], "labels": []}
    time_pattern = mappings.group_type__pattern[group_type]
    dt_from = datetime.datetime.strptime(dt_from.strftime(time_pattern), time_pattern)
    dt_upto = datetime.datetime.strptime(dt_upto.strftime(time_pattern), time_pattern)

    cur_dt = dt_from
    delta = mappings.group_type__delta[group_type]
    async for d in results:
        next_val = d["totalValue"]
        next_dt = d["label"]
        while next_dt != cur_dt:
            output["dataset"].append(0)
            output["labels"].append(cur_dt.isoformat())
            cur_dt += delta

        output["dataset"].append(next_val)
        output["labels"].append(next_dt.isoformat())
        cur_dt += delta

    while cur_dt <= dt_upto:
        output["dataset"].append(0)
        output["labels"].append(cur_dt.isoformat())
        cur_dt += delta

    return output
