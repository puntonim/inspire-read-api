from ..models.inspirehep import RecordMetadata
from . import exceptions
from .record_metadata_base import (
    RecordMetadataDetailDomainBase, RecordMetadataListDomainBase)


class AuthorsListDomain(RecordMetadataListDomainBase):
    def get_queryset(self):
        # Always return ordered querysets because they will be paginated
        # later on.
        queryset = RecordMetadata.author_objects.all().order_by('id')

        # Query filters.
        literature_recid = self.query_params_parser.literature
        if literature_recid:
            queryset = queryset.filter_by_literature(literature_recid)

        return queryset
