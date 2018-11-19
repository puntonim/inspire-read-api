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
    def fields_extra(self):
        fields_extra_string = self.query_params.get('fields-extra', '')
        # Split by , and filter out falsy.
        return list(filter(bool, fields_extra_string.split(',')))

    @property
    def token_field_extra(self):
        return 'token' in self.fields_extra

    @property
    def author_field_extra(self):
        return 'author' in self.fields_extra

    @property
    def literature(self):
        return self.query_params.get('literature', '')

    @property
    def author(self):
        return self.query_params.get('author', '')

    @property
    def orcid(self):
        return self.query_params.get('orcid', '')

    @property
    def push(self):
        value = self.query_params.get('push', '')
        if value.lower() in ['true', 't', 'yes', 'y', '1']:
            return True
        elif value.lower() in ['false', 'f', 'no', 'n', '0']:
            return False
        else:
            return None


class QueryParamsParserMixin:
    """
    To be used in a typical view in combination with a (subclass of)
    rest_framework.views.APIView.
    """
    def initial(self, *args, **kwargs):
        self.query_params_parser = QueryParamsParser(self.request.query_params)
        return super().initial(*args, **kwargs)
