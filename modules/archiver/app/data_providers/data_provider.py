# The Data Provider acts as the abstract class for the datasources feeding into
# the archiver data warehouse.
# from abc import abstractmethod, ABCMeta


class DataProvider:
    data_providers = []

    def __init__(self):
        self.data_providers.append(self)

    # @abstractmethod
    def schedule(self):
        raise NotImplementedError