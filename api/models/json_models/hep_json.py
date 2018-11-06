"""
HepJson model encapsulates the logic to access RecordMetadata.json data for
a hep.json $schema.
"""
import utils.data

from .embedded.author_embedded import AuthorEmbedded


class HepJson(utils.data.SmartgetDictMixin):
    @property
    def authors_embedded(self):
        return [AuthorEmbedded(a) for a in self.smartget('authors', [])]

    @property
    def curated_authors_embedded(self):
        return [a for a in self.authors_embedded if a.is_curated]
