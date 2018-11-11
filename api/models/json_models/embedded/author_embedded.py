import utils.data

from .orcid_embedded import OrcidEmbedded


class AuthorEmbedded(utils.data.SmartgetDictMixin):
    """
    A dictionary like:
        {
            "ids": [
                {
                    "value": "M.Maciejewski.1",
                    "schema": "INSPIRE BAI"
                }
            ],
            "uuid": "0fdff9b4-9a5c-4f63-8f42-5047b5e89d00",
            "record": {
                "$ref": "http://labs.inspirehep.net/api/authors/7780"
            },
            "value": "Maciejewski, Micha",
            "signature_block": "MASTARk",
            "curated_relation": true
        }
    """
    @property
    def is_curated(self):
        return self.smartget('curated_relation', False)

    @property
    def orcid_embedded(self):
        orcids = self.smartget_if('ids', lambda id: id['schema'].upper()=='ORCID' if id else False)
        if not orcids:
            return None
        if len(orcids) > 1:
            # TODO specific exception
            raise Exception('This guy has #{} orcids, too many!'.format(len(orcids)))
        return OrcidEmbedded(orcids[0])

    @property
    def all_orcids_embedded(self):
        """
        The OrcidEmbedded in the AuthorEmbedded.
        Plus the OrcidEmbedded in the actual author record.
        """
        results = [self.orcid_embedded]
        # Business rule: the author must be curated in order to consider her
        # author_record_metadata.json_model.orcid_embedded.
        if self.is_curated and self.recid:
            results.append(self.author_record_metadata.json_model.orcid_embedded)
        results = list(filter(bool, results))
        # Ensure all orcids actually have the same value.
        if len(results) > 1:
            for i in range(len(results)-1):
                if results[i]['value'] != results[i+1]['value']:
                    # TODO specific exception
                    raise Exception('This guy have multiple different orcids')
        return results

    @property
    def orcid_identity(self):
        for orcid_embedded in self.all_orcids_embedded:
            if orcid_embedded.orcid_identity:
                return orcid_embedded.orcid_identity

    @property
    def recid(self):
        ref = self.smartget('record.$ref')  # Format: 'http://labs.inspirehep.net/api/authors/1016652'
        if not ref:
            return None
        return int(ref.split('/')[-1])

    @property
    def author_record_metadata(self):
        from api.models.inspirehep import RecordMetadata
        if not self.recid:
            return None
        return RecordMetadata.author_objects.get_by_pid(self.recid)
