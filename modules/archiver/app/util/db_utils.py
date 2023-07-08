from pymongo import DuplicateKeyError


class DbUtils:
    @staticmethod
    def safe_insert(collection, data): 
        try: 
            collection.insert_one(data)
        except DuplicateKeyError as e:
            print(e)