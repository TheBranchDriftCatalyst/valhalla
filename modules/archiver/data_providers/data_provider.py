# The Data Provider acts as the abstract class for the datasources feeding into
# the archiver data warehouse.
from abc import abstractmethod, ABCMeta

from modules.brainz.src.archiver.db.s3_storage_connector import S3StorageConnector


class DataProvider(ABCMeta):
    @classmethod
    def initialize_data_providers(mcs, providers: list[dict]):
        print(mcs)

    def __init__(self):
        super().__init__(self)

    @abstractmethod
    def schedule(self):
        raise NotImplementedError

    def save_record(self, provider_name=string) -> bool:
        return S3StorageConnector.save_record()

    @abstractmethod
    def get_labels(self) -> dict:
        raise NotImplementedError
