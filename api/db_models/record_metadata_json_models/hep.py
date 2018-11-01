"""
Hep model encapsulate the logic to access RecordMetadata.json data for a hep.json $schema.
"""
import utils.data


class HepJson(utils.data.SmartgetDictMixin):
    @property
    def authors_enclosed(self):
        return [AuthorEnclosed(a) for a in self.smartget('authors', [])]

    @property
    def curated_authors_enclosed(self):
        return [a for a in self.authors_enclosed if a.is_curated]


class AuthorEnclosed(utils.data.SmartgetDictMixin):
    @property
    def is_curated(self):
        return self.smartget('curated_relation', False)

    @property
    def has_orcid_enclosed(self):
        return bool(self.orcid_enclosed)

    @property
    def orcid_enclosed(self):
        orcids = self.smartget_if('ids', lambda id: id['schema'].upper()=='ORCID' if id else False)
        if not orcids:
            return None
        if len(orcids) > 1:
            raise Exception('This guy has #{} orcids, too many!'.format(len(orcids)))  # TODO
        return orcids[0]['value']

    @property
    def has_orcid_identity(self):
        return bool(self.orcid_identity)

    @property
    def orcid_identity(self):
        """
        Not all orcid_enclosed have a matching OrcidIdentity.
        Typically there is a OrcidIdentity if the author has logged in in Legacy
        or Labs with her ORCID.
        """
        return self.record_metadata.json_model.orcid_identity

    @property
    def has_recid(self):
        return bool(self.recid)

    @property
    def recid(self):
        ref = self.smartget('record.$ref')  # Format: 'http://labs.inspirehep.net/api/authors/1016652'
        if not ref:
            return None
        return int(ref.split('/')[-1])

    @property
    def record_metadata(self):
        from ..inspirehep import RecordMetadata
        if not self.has_recid:
            return None
        return RecordMetadata.author_objects.get_by_pid(self.recid)
