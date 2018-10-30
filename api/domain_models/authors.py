from ..db_models.inspirehep import RecordMetadata, PidstorePid

from .record_metadata_base import RecordMetadataDetailDomainBase
from .query_params import QueryParamsParser


class AuthorDetailDomain(RecordMetadataDetailDomainBase):
    def get_object(self):
        return RecordMetadata.objects.get_by_pid(self.pid_value, pid_type=PidstorePid.TYPE_AUT)


class AuthorsListDomain:
    def __init__(self, query_params):
        self.query_params_parser = QueryParamsParser(query_params)

    def get_queryset(self):
        # Query filters.
        literature_recid = self.query_params_parser.literature()
        if literature_recid:
            literature = RecordMetadata.literature.get_by_pid(literature_recid)
            queryset = [x.record_metadata for x in literature.json_model.authors]
        else:
            queryset = RecordMetadata.authors.all()
        return queryset

    def get_paginated_data(self, raw_data):
        # TODO filter json fields as in RecordMetadataDetailDomainBase.get_data(), maybe make a common method
        for record in raw_data:
            record.json = {
                'control_number': record.json['control_number'],
            }
        return raw_data