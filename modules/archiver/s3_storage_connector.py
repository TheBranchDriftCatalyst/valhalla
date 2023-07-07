import boto3


class S3StorageConnector:
    def __init__(self, bucket_name):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the connection to S3 and stores the bucket name for later use.

        :param self: Represent the instance of the class
        :param bucket_name: Specify the name of the bucket to be created
        :return: The instance of the class
        :doc-author: Trelent
        """
        self.s3 = boto3.resource(
            "s3",
            endpoint_url="https://<minio>:9000",
            aws_access_key_id="<key_id>",
            aws_secret_access_key="<access_key>",
            aws_session_token=None,
            config=boto3.session.Config(signature_version="s3v4"),
            verify=False,
        )
        self.bucket_name = bucket_name

    def upload(self, key, data):
        """
        The upload function takes a key and data as input.
        The function then uploads the data to the S3 bucket using the given key.

        :param self: Represent the instance of the class
        :param key: Specify the name of the file to be uploaded
        :param data: Pass the data to be uploaded
        :return: None
        :doc-author: Trelent
        """
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=data)

    def download(self, key):
        """
        The download function takes a key as an argument and returns the contents of that file.
        The function uses the boto3 library to access AWS S3, which is a cloud storage service.
        It first creates an s3 client object using boto3's resource method, then it calls get_object on that client object with
        the bucket name and key as arguments. The get_object method returns a dictionary containing metadata about the file
        and its contents (in this case we only care about its contents). We can access those by calling ['Body'].read().

        :param self: Represent the instance of the class
        :param key: Specify the file you want to download
        :return: The body of the object as bytes
        :doc-author: Trelent
        """
        return self.s3.get_object(Bucket=self.bucket_name, Key=key)["Body"].read()

    def delete(self, key):
        """
        The delete function deletes a file from the S3 bucket.

        :param self: Represent the instance of the class
        :param key: Specify the name of the object to delete
        :return: Nothing
        :doc-author: Trelent
        """
        self.s3.delete_object(Bucket=self.bucket_name, Key=key)

    def list(self, prefix):
        """
        The list function takes a prefix as an argument and returns a list of all the keys in the bucket that start with that prefix.
        The function uses boto3's list_objects method to get all objects in the bucket, then filters out any objects whose key doesn't start with our desired prefix.

        :param self: Represent the instance of the class
        :param prefix: Filter the objects returned to those whose names begin with the prefix
        :return: A list of all the keys in a bucket
        :doc-author: Trelent
        """
        return [
            obj["Key"]
            for obj in self.s3.list_objects(Bucket=self.bucket_name, Prefix=prefix)[
                "Contents"
            ]
        ]
