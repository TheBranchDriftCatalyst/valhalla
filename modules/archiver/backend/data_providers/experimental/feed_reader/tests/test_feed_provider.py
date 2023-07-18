import unittest

from feed_reader.feed_provider import FeedProvider


class TestFeedProvider(unittest.TestCase):
    def test_fetch_articles_urls_from_feed(self):
        feed_provider = FeedProvider("https://www.hackthebox.eu/feed")
        articles = feed_provider.fetch_articles_urls_from_feed()
        self.assertGreaterEqual(len(articles), 25)

    def test_get_article(self):
        feed_provider = FeedProvider("ht")
        articles = feed_provider.fetch_articles_urls_from_feed("https://www.hackthebox.eu/feed")
        article = feed_provider.get_article(articles[0])
        self.assertIsNotNone(article)


if __name__ == "__main__":
    unittest.main()
