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
    def has_orcid_user_identity(self):
        return bool(self.orcid_user_identity)

    @property
    def orcid_user_identity(self):
        """
        Not all orcid_enclosed have a matching UserIdentity.
        Typically there is a UserIdentity if the author has logged in in Legacy
        or Labs with his ORCID.
        """
        from ..inspirehep import UserIdentity
        if not self.has_orcid_enclosed:
            return None
        try:
            return UserIdentity.orcid_objects.get(id=self.orcid_enclosed)
        except UserIdentity.DoesNotExist:
            return None

