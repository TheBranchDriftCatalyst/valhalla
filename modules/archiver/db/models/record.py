from mongoengine import *

connect('archiver', host='mongodb://localhost:27017')

# Define the model for RecordMetaData
class RecordMetaData(Document):
    id: UUIDField()
    article_date = DateTimeField()
    labels = ListField(StringField())


# Define the model for Record
class Record(Document):
    id: UUIDField()
    s3_bucket_name = URLField()
    s3_record_key = StringField()
    retrieved_at = DateTimeField()
    source = URLField()
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"


class NewsArticle(Document):
    id: UUIDField()
    content = StringField()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"
