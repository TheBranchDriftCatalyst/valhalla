from logging import getLogger

from app.storage_connectors.s3_storage_connector import S3StorageConnector


class Archiver:
    def __init__(self, config, db):
        self.s3_connector = S3StorageConnector(config["s3_bucket_name"])
        # self.mongo_connector = MongoConnector(config["mongo_uri"])
        self.mongo_connector = {}
        self.log = getLogger(__name__)

    def upload(self, key, data):
        """
        The upload function uploads a file to S3.

        :param self: Represent the instance of the class
        :param key: Specify the name of the file to be uploaded
        :param data: Pass the data to be uploaded
        :return: None, which is the default return value for functions in python
        :doc-author: Trelent
        """
        self.s3_connector.upload(key, data)
        self.log.info(f"Uploaded {key} to S3")
        # self.mongo_connector.save_record(key, data)

    def download(self, key):
        """
        The download function takes a key as an argument and returns the S3 record
        and MongoDB record associated with that key. The function first downloads the
        S3 object using the download method of our S3Connector class, then uses
        the get_record method of our MongoDBConnector class to retrieve the corresponding
        MongoDB document.

        :param self: Represent the instance of the class
        :param key: Identify the record in both s3 and mongodb
        :return: A tuple of s3_record and mongo_record
        :doc-author: Trelent
        """
        s3_record = self.s3_connector.download(key)
        mongo_record = self.mongo_connector.get_record(key)
        return s3_record, mongo_record

    def validate_db_consistency(self):
        """
        The validate_db_consistency function checks that the S3 and Mongo databases are consistent.
        It does this by comparing the set of keys in each database, and raising an exception if they do not match.

        :param self: Represent the instance of the class
        :return: True if the s3 and mongodb are consistent, otherwise it raises an exception
        :doc-author: Trelent
        """
        s3_keys = self.s3_connector.list("")
        mongo_keys = self.mongo_connector.get_all_record_keys()
        if set(s3_keys) != set(mongo_keys):
            raise Exception("S3 and Mongo are not consistent")

    def prune_orphaned_records(self):
        """
        The prune_orphaned_records function is used to delete records from the MongoDB database that are no longer present in S3.
        This function is useful for cleaning up after a failed upload or deletion of an object from S3, as well as for keeping the
        MongoDB database clean and free of orphaned records.

        :param self: Refer to the object itself
        :return: Nothing
        :doc-author: Trelent
        """
        s3_keys = self.s3_connector.list("")
        mongo_keys = self.mongo_connector.get_all_record_keys()
        for key in set(mongo_keys) - set(s3_keys):
            self.mongo_connector.delete_record(key)
            self.log.info(f"Deleted {key} from Mongo")
        self.log.info("Finished pruning orphaned records")

    def delete(self, key):
        """
        The delete function takes a key as an argument and deletes the corresponding record from S3 and Mongo.
        It returns nothing.

        :param self: Represent the instance of the class
        :param key: Specify the key of the object to delete
        :return: None
        :doc-author: Trelent
        """
        self.s3_connector.delete(key)
        self.mongo_connector.delete_record(key)
        self.log.info(f"Deleted {key} from S3 and Mongo")
