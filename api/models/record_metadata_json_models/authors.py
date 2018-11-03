"""
AuthorJson model encapsulates the logic to access RecordMetadata.json data for
a authors.json $schema.
"""
import utils.data


class AuthorJson(utils.data.SmartgetDictMixin):
    @property
    def has_orcid_embedded(self):
        return bool(self.orcid_embedded)

    @property
    def orcid_embedded(self):
        orcids = self.smartget_if('ids', lambda id: id['schema'].upper()=='ORCID')
        if not orcids:
            return None
        if len(orcids) > 1:
            raise Exception('This guy has {} orcids'.format(len(orcids)))
        return orcids[0]['value']

    @property
    def has_orcid_identity(self):
        return bool(self.orcid_identity)

    @property
    def orcid_identity(self):
        """
        Not all orcid_embedded have a matching OrcidIdentity.
        Typically there is a OrcidIdentity if the author has logged in in Legacy
        or Labs with his ORCID.
        """
        from ..inspirehep import OrcidIdentity
        if not self.has_orcid_embedded:
            return None
        try:
            return OrcidIdentity.objects.get(orcid_value=self.orcid_embedded)
        except OrcidIdentity.DoesNotExist:
            return None
