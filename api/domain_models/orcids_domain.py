from ..models.inspirehep import RecordMetadata, OrcidIdentity

from .record_metadata_base import (
    RecordMetadataListDomainBase)


class OrcidIdentitiesListDomain(RecordMetadataListDomainBase):
    def __init__(self, query_params_parser):
        self.query_params_parser = query_params_parser

    def get_queryset(self):
        # Always return ordered querysets because they will be paginated
        # later on.
        queryset = OrcidIdentity.objects.all().order_by('id')

        # Query filters.
        # Literature: ?literature=1126991
        literature_recid = self.query_params_parser.literature
        if literature_recid:
            queryset = queryset.filter_by_authored_literature(literature_recid)

        # Author: ?author=1126991
        author_recid = self.query_params_parser.author
        if author_recid:
            try:
                orcid_identity = queryset.get_by_author(author_recid)
                queryset = queryset.filter(id=orcid_identity.id)
            except RecordMetadata.DoesNotExist:
                queryset = queryset.filter(id=None)

        # Push: ?push=true
        do_push = self.query_params_parser.push
        if do_push is not None:
            queryset = queryset.filter_by_allow_push(do_push)

        return queryset
