class MongoStorageConnector:

    def __init__(self, mongo_url, mongo_db, mongo_collection):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.client = None
        self.db = None
        self.collection = None
