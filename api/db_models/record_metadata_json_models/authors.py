"""
Author model encapsulate the logic to access RecordMetadata.json data for a authors.json $schema.
"""
import utils.data


class AuthorJson(utils.data.SmartgetDictMixin):
    @property
    def has_orcid_enclosed(self):
        return bool(self.orcid_enclosed)

    @property
    def orcid_enclosed(self):
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
    def orcid_user_identity(self):
        """
        Not all orcid_enclosed have a matching OrcidIdentity.
        Typically there is a OrcidIdentity if the author has logged in in Legacy
        or Labs with his ORCID.
        """
        from ..inspirehep import OrcidIdentity
        if not self.has_orcid_enclosed:
            return None
        try:
            return OrcidIdentity.objects.get(orcid_value=self.orcid_enclosed)
        except OrcidIdentity.DoesNotExist:
            return None
