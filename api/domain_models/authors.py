from ..db_models.inspirehep import RecordMetadata

from .record_metadata_base import (
    RecordMetadataDetailDomainBase, RecordMetadataListDomainBase)


class AuthorDetailDomain(RecordMetadataDetailDomainBase):
    def get_object(self):
        return RecordMetadata.author_objects.get_by_pid(self.pid_value)


class AuthorsListDomain(RecordMetadataListDomainBase):
    def get_queryset(self):
        # Query filters.
        literature_recid = self.query_params_parser.literature
        if literature_recid:
            return RecordMetadata.author_objects.filter_by_literature(literature_recid)
        else:
            queryset = RecordMetadata.author_objects.all()
        return queryset
