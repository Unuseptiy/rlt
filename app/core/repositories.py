from pymongo.collection import Collection


class SampleCollectionRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def aggregate(self, pipeline):
        return self.collection.aggregate(pipeline)
