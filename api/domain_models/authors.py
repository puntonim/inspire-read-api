from ..models.inspirehep import RecordMetadata
from . import exceptions
from .record_metadata_base import (
    RecordMetadataDetailDomainBase, RecordMetadataListDomainBase)


class AuthorsListDomain(RecordMetadataListDomainBase):
    def get_queryset(self):
        # Note: always return ordered querysets because they will be paginated
        # later on.
        # Query filters.
        literature_recid = self.query_params_parser.literature
        if literature_recid:
            try:
                queryset = RecordMetadata.author_objects\
                    .filter_by_literature(literature_recid)\
                    .order_by('id')
            except RecordMetadata.DoesNotExist:
                queryset = []

        else:
            queryset = RecordMetadata.author_objects.all().order_by('id')
        return queryset
