from ..models.inspirehep import RecordMetadata
from . import exceptions
from .record_metadata_base import (
    RecordMetadataDetailDomainBase, RecordMetadataListDomainBase)


class LiteratureListDomain(RecordMetadataListDomainBase):
    def get_queryset(self):
        # Always return ordered querysets because they will be paginated
        # later on.
        queryset = RecordMetadata.literature_objects.all().order_by('id')

        # Query filters.
        # Author: ?author=1126991
        author_recid = self.query_params_parser.author
        if author_recid:
            queryset = queryset.filter_by_author(author_recid)

        return queryset
