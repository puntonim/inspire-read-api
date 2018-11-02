from ..models.inspirehep import RecordMetadata
from .query_params import QueryParamsParser


def filter_record_json_by_fields(record, fields_include):
    record_json_keys = list(record.json.keys())

    if not fields_include:
        return

    for key in record_json_keys:
        if key not in fields_include:
            del record.json[key]


class RecordMetadataDetailDomainBase:
    def __init__(self, pid_value, query_params):
        self.pid_value = pid_value
        self.query_params_parser = QueryParamsParser(query_params)

    def get_object(self):
        return RecordMetadata.objects.get_by_pid(self.pid_value)

    def get_data(self):
        record = self.get_object()
        filter_record_json_by_fields(record, self.query_params_parser.fields_include)
        return record


class RecordMetadataListDomainBase:
    def __init__(self, query_params):
        self.query_params_parser = QueryParamsParser(query_params)

    def get_paginated_data(self, raw_data):
        for record in raw_data:
            filter_record_json_by_fields(record, self.query_params_parser.fields_include)
        return raw_data
