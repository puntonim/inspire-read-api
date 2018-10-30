from ..db_models.inspirehep import RecordMetadata
from .query_params import QueryParamsParser


class RecordMetadataDetailDomainBase:
    def __init__(self, pid_value, query_params):
        self.pid_value = pid_value
        self.query_params_parser = QueryParamsParser(query_params)

    def get_object(self):
        return RecordMetadata.objects.get_by_pid(self.pid_value)

    def get_data(self):
        record = self.get_object()
        record_json_keys = list(record.json.keys())

        if self.query_params_parser.fields_include:
            for key in record_json_keys:
                if key not in self.query_params_parser.fields_include:
                    del record.json[key]

        return record
