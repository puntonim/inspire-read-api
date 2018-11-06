import utils.data


class OrcidEmbedded(utils.data.SmartgetDictMixin):
    """
    A dictionary like:
        {
            "value": "0000-0002-4133-9999",
            "schema": "ORCID"
        }
    """
    @property
    def has_orcid_identity(self):
        return bool(self.orcid_identity)

    @property
    def orcid_identity(self):
        """
        Not all OrcidEmbedded have a matching OrcidIdentity.
        Typically there is a OrcidIdentity if the author has logged in in Legacy
        or Labs with her ORCID.
        """
        from api.models.inspirehep import OrcidIdentity
        try:
            return OrcidIdentity.objects.get(orcid_value=self['value'])
        except OrcidIdentity.DoesNotExist:
            return None
