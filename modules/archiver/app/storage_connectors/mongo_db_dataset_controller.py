import os
from pymongo import MongoClient, ASCENDING
from app.util import IndifferentAccessDict
import pymongo

class MongoDBDatasetController:
    def __init__(self, dataset_name: str, dataset_collections: list[str], env=None) -> "MongoDBDatasetController":
        self.env = env or os.environ.get("ENV", "dev")
        self.dataset_name = dataset_name
        
        self.db = MongoClient(f"mongodb://localhost:27017/{self.env}")

        self.collections = IndifferentAccessDict(dict(map(lambda x: (x[0], self.db[x[0]]), dataset_collections)))
