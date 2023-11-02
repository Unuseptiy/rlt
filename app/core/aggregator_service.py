import datetime

from pymongo.collection import Collection

from app.core import mappings, utils
from app.schemas import GroupType


def aggregate(
    dt_from: datetime.datetime,
    dt_upto: datetime.datetime,
    group_type: GroupType,
    collection: Collection,
) -> dict[str, list]:
    """
    Salary aggregator.
    :param dt_from: start aggregation datetime
    :type dt_from: datetime.datetime
    :param dt_upto: end aggregation datetime
    :type dt_upto: datetime.datetime
    :param group_type: aggregation type
    :type group_type: GroupType
    :param collection: MongoDB Collection
    :type collection: pymongo.collection.Collection


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
    results = collection.aggregate(pipeline)
    output = utils.prepare_result(results, dt_from, dt_upto, group_type)

    return output
