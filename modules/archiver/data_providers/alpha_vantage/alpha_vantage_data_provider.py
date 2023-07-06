from src.archiver.data_providers.data_provider import DataProvider


class AlphaVantageDataProvider(DataProvider):
    DEFAULT_CONFIG = {
        "url": "https://www.bbc.co.uk/news/technology/rss.xml",
        "labels": {
            "source": "bbc",
            "category": "technology",
        },
        "tickers": ["MSFT"],
        "api_key": "7KAGLU9OTBWYRQJQ",
    }

    def __init__(self, api_key: str, labels: dict, tickers: list[str]):
        super().__init__()
        self.labels = labels
        self.api_key = api_key
        self.tickers = tickers

    def schedule(self):
        pass

    def get_data(self):

        # save_rezcord()
        pass

    def save_data(self):
        super.save_record()
