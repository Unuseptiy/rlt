import datetime
from collections.abc import Coroutine

from app.core import mappings, utils
from app.core.repositories import SampleCollectionRepository
from app.schemas import GroupType


async def aggregate(
    dt_from: datetime.datetime,
    dt_upto: datetime.datetime,
    group_type: GroupType,
    sample_collection_repository: SampleCollectionRepository,
) -> Coroutine[None, None, dict[str, list]]:
    """
    Salary aggregator.
    :param dt_from: start aggregation datetime
    :type dt_from: datetime.datetime
    :param dt_upto: end aggregation datetime
    :type dt_upto: datetime.datetime
    :param group_type: aggregation type
    :type group_type: GroupType
    :param sample_collection_repository: Sample Collection Repository
    :type sample_collection_repository: SampleCollectionRepository


    :rtype: dict
    :return: dict with aggregated data and labels for corresponding data
    """
    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lt": dt_upto}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": mappings.group_type__pattern[group_type],
                        "date": "$dt",
                    }
                },
                "totalValue": {"$sum": "$value"},
            }
        },
        {"$sort": {"_id": 1}},
        {"$addFields": {"label": {"$dateFromString": {"dateString": "$_id"}}}},
    ]
    results = sample_collection_repository.aggregate(pipeline)
    output = await utils.prepare_result(results, dt_from, dt_upto, group_type)

    return output
