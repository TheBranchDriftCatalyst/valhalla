class DataProvider:
    DATA_PROVIDERS = []

    def __init__(self):
        self.DATA_PROVIDERS.append(self)

    @classmethod
    def schedule(cls):
        raise NotImplementedError