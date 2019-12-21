from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from core.models import Book, Author


# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])


INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class BookDocument(Document):
    author = fields.ObjectField(properties={
        'name': fields.TextField(),
        'email': fields.TextField()
    })

    class Django:
        model = Book

        fields = [
            'name',
            'created_on',
        ]

    class Index:
        name = 'books'
