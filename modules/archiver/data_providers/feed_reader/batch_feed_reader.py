import feedparser
import concurrent.futures


class BatchFeedReader:
    def __init__(self, feed_providers):
        """
        The __init__ function is called when the class is instantiated.
        It takes a list of urls as an argument and sets it to self.urls, which means that it will be available to all other functions in the class.

        :param self: Represent the instance of the class
        :param urls: Store the list of urls that will be passed to the constructor
        :return: The self object
        :doc-author: Trelent
        """
        self.feed_providers = feed_providers

    def fetch(self, url):
        feed = feedparser.parse(url)
        article_urls = [entry['link'] for entry in feed['entries']]
        return [feed, labels]

    def mt_fetch(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.fetch, self.urls)







BatchFeedReader(feed_urls).mt_fetch()
