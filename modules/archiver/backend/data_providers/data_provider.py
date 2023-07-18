class DataProvider:
    DATA_PROVIDERS = set()

    def __init__(self):
        self.DATA_PROVIDERS.add(__name__)

    @classmethod
    def schedule(cls):
        raise NotImplementedError
    
    #  One or the other
    def run(self):
        raise NotImplementedError
    
    def listen(self):
        raise NotImplementedError