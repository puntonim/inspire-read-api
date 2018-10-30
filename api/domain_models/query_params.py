from django.utils.functional import cached_property


class QueryParamsParser:
    def __init__(self, query_params):
        self.query_params = query_params

    @cached_property
    def fields_include(self):
        fields_include_string = self.query_params.get('fields-include', '')
        # Split by , and filter out falsy.
        return list(filter(bool, fields_include_string.split(',')))

    @property
    def literature(self):
        return self.query_params.get('literature', '')

    @property
    def push(self):
        value = self.query_params.get('push', '')
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            return None
