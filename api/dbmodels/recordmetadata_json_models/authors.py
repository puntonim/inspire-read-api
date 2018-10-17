"""
Author model encapsulate the logic to access RecordMetadata.json data for a authors.json $schema.
"""
import utils.data

### es. 1606373
class AuthorJson(utils.data.SmartgetDictMixin):
    @property
    def has_orcid(self):
        return bool(self.orcid)

    @property
    def orcid(self):
        orcids = self.smartget_if('ids', lambda id: id['schema'].upper()=='ORCID')
        if not orcids:
            return None
        if len(orcids) > 1:
            raise Exception('This guy has {} orcids'.format(len(orcids)))
        return orcids[0]['value']
