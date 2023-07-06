import string
import feedparser
import newspaper
from logging import getLogger


# This should not change but
def get_article_links(feed_entry):
    return feed_entry["link"]


class FeedProvider:
    def __init__(self, feed_url, feed_source_labels=None, fetcher=lambda x: x):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the logger and labels for this instance of the class.

        :param self: Represent the instance of the class
        :param feed_url: string: Set the feed_url attribute of the class
        :param feed_source_labels: Specify the labels that are used to classify the articles on this feed
        :param fetcher: Specify the function that is used to fetch the articles the links to articles from the feed
        :return: Nothing
        :doc-author: Trelent
        """
        self.logger = getLogger(__name__)
        self.logger.setLevel("DEBUG")
        if feed_source_labels is None:
            feed_source_labels = {}
        self.feed_source_labels = feed_source_labels
        self.feed_url = feed_url
        self.fetcher = fetcher

    def fetch_articles_urls_from_feed(self) -> list[str]:
        """
        The fetch_articles_urls_from_feed function takes a feed URL and returns a list of article URLs.

        :param self: Represent the instance of the class
        :return: A list of article links
        :doc-author: Trelent
        """
        feed = feedparser.parse(self.feed_url)
        article_urls = [get_article_links(entry) for entry in feed["entries"]]
        self.logger.info(f"Found {len(article_urls)} articles in feed {self.feed_url}")
        self.logger.debug(f"article_urls: {article_urls}")
        return article_urls

    def get_article(self, article_url):
        """
        The get_article function takes an article_url and returns a parsed newspaper.Article object.

        :param self: Represent the instance of the class
        :param article_url: Download the article from the newspaper library
        :return: The parsed article
        :doc-author: Trelent
        """
        article = newspaper.Article(article_url)
        article.download()
        parsed_article = article.parse()
        self.logger.info(
            f"Downloaded and parsed article {article_url} from feed {self.feed_url}"
        )
        self.logger.debug(f"parsed_article: {parsed_article}")
        return parsed_article
