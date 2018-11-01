from ..db_models.inspirehep import RecordMetadata, OrcidIdentity

from .query_params import QueryParamsParser
from .record_metadata_base import (
    RecordMetadataDetailDomainBase, RecordMetadataListDomainBase)


class OrcidIdentitiesListDomain(RecordMetadataListDomainBase):
    def __init__(self, query_params):
        self.query_params_parser = QueryParamsParser(query_params)

    def get_queryset(self):
        # Query filters.
        literature_recid = self.query_params_parser.literature
        if literature_recid:
            queryset = OrcidIdentity.objects.filter_by_authored_literature(literature_recid)
        else:
            queryset = OrcidIdentity.objects.all()
        return queryset
