import os
import mimetypes
# from examples.progress import Progress
from minio import Minio
from minio.error import InvalidResponseError

class S3StorageController:
    # TODO: move these to ENV shortly
    def __init__(self, endpoint='localhost:9000', access_key="turbopanda666", secret_key="turbopanda666"):
        self.client = Minio(
            endpoint, 
            access_key=access_key, 
            secret_key=secret_key
        )
            
    def put_file(self, bucket_name, object_name, file_path, content_type=None):
        # Put a file with 'application/csv'
        try:
            with open(file_path, 'rb') as file_data:
                file_stat = os.stat(file_path)
                file_type = content_type or mimetypes.guess_type(file_path) or 'application/octet-stream'
                self.client.put_object(
                    bucket_name, 
                    object_name, 
                    file_data, 
                    file_stat.st_size, 
                    content_type=content_type # type: ignore
                )
        except InvalidResponseError as err:
            print(err)


# Put a file with progress.
# progress = Progress()
# try:
#     with open('my-testfile', 'rb') as file_data:
#         file_stat = os.stat('my-testfile')
#         client.put_object('my-bucketname', 'my-objectname',
#                           file_data, file_stat.st_size, progress=progress)
# except ResponseError as err:
#     print(err)