"""
AuthorJson model encapsulates the logic to access RecordMetadata.json data for
a authors.json $schema.
"""
import utils.data

from .embedded.orcid_embedded import OrcidEmbedded


class AuthorJson(utils.data.SmartgetDictMixin):
    @property
    def has_orcid_embedded(self):
        return bool(self.orcid_embedded)

    @property
    def orcid_embedded(self):
        orcids = self.smartget_if('ids', lambda id: id['schema'].upper()=='ORCID' if id else False)
        if not orcids:
            return None
        if len(orcids) > 1:
            # TODO specific exception
            raise Exception('This guy has {} orcids'.format(len(orcids)))
        return OrcidEmbedded(orcids[0])
