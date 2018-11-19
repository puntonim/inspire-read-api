from ..models.inspirehep import RecordMetadata, OrcidIdentity
from . import exceptions
from .record_metadata_base import RecordMetadataListDomainBase


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


class OrcidIdentityDetailDomain:
    def __init__(self, orcid_value, query_params_parser):
        self.orcid_value = orcid_value
        self.query_params_parser = query_params_parser

    def get_object(self):
        try:
            return OrcidIdentity.objects.get(orcid_value=self.orcid_value)
        except OrcidIdentity.DoesNotExist as exc:
            msg = 'OrcidIdentity with orcid_value={} does not exist'.format(
                self.orcid_value)
            raise exceptions.OrcidIdentityDoesNotExist(msg) from exc

    def get_data(self):
        object = self.get_object()
        # Query filters: fields-extra.
        author = self.query_params_parser.author_field_extra
        if author is not None:
            authors = RecordMetadata.author_objects\
                .filter_by_orcid_embedded(self.orcid_value)
            if not authors:
                object.author_pid = None
            elif authors.count() > 1:
                raise Exception  # TODO
            else:
                author = authors[0]
                object.author_pid = author.control_number

        return object
