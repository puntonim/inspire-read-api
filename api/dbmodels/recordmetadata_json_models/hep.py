"""
Hep model encapsulate the logic to access RecordMetadata.json data for a hep.json $schema.
"""
import utils.data


class HepJson(utils.data.SmartgetDictMixin):
    @property
    def authors(self):
        return [Author(a) for a in self.smartget('authors')]

    @property
    def curated_authors(self):
        return [a for a in self.authors if a.is_curated]


class Author(utils.data.SmartgetDictMixin):
    @property
    def is_curated(self):
        return self.smartget('curated_relation', False)

    @property
    def has_orcid(self):
        return bool(self.orcid)

    @property
    def orcid(self):
        orcids = self.smartget_if('ids', lambda id: id['schema'].upper()=='ORCID' if id else False)
        if not orcids:
            return None
        if len(orcids) > 1:
            raise Exception('This guy has {} orcids'.format(len(orcids)))
        return orcids[0]['value']

    @property
    def has_record(self):
        return bool(self.recid)

    @property
    def recid(self):
        ref = self.smartget('record.$ref')  # Format: 'http://labs.inspirehep.net/api/authors/1016652'
        if not ref:
            return None
        return int(ref.split('/')[-1])

    @property
    def record_metadata(self):
        from ..inspirehep import PidstorePid, RecordMetadata
        if not self.has_record:
            return None
        return RecordMetadata.objects.get_by_pid(self.recid, pid_type=PidstorePid.TYPE_AUT)
