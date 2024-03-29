from django.http import JsonResponse
from django.utils import timezone

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from . import serializers
from .domain_models.record_metadata_base import RecordMetadataDetailDomainBase
from .domain_models.authors_domain import AuthorsListDomain
from .domain_models.literature_domain import LiteratureListDomain
from .domain_models.orcids_domain import OrcidIdentitiesListDomain, OrcidIdentityDetailDomain
from .domain_models import exceptions as domain_exceptions
from .query_params import QueryParamsParserMixin


def health(request):
    now = timezone.localtime(timezone.now())
    return JsonResponse({'date': now})


def unhealth(request):
    class UnhealthTestException(Exception):
        pass

    now = timezone.localtime(timezone.now())
    raise UnhealthTestException('/unhealth endpoint called on {}'.format(now))
    return 'It should have raised UnhealthTestException'


class LiteratureDetail(QueryParamsParserMixin, generics.RetrieveAPIView):
    """
    $ curl 127.0.0.1:8000/api/literature/335152/?fields-include=titles,control_number
    """
    serializer_class = serializers.RecordMetadataSerializer
    domain_model_class = RecordMetadataDetailDomainBase
    pid_type = 'lit'

    def retrieve(self, request, *args, **kwargs):
        domain = self.domain_model_class(
            pid_type=self.pid_type,
            pid_value=self.kwargs['pid_value'],
            query_params_parser=self.query_params_parser
        )
        try:
            data = domain.get_data()
        except domain_exceptions.RecordMetadataDoesNotExist:
            raise NotFound
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class LiteratureList(QueryParamsParserMixin, generics.ListAPIView):
    """
    $ curl "127.0.0.1:8000/api/literature/?author=1607170&fields-include=titles"
    """
    serializer_class = serializers.RecordMetadataSerializer
    domain_model_class = LiteratureListDomain

    def get_queryset(self, *args, **kwargs):
        self.domain_model = self.domain_model_class(
            query_params_parser=self.query_params_parser
        )
        return self.domain_model.get_queryset()

    def paginate_queryset(self, *args, **kwargs):
        raw_data = super().paginate_queryset(*args, **kwargs)
        try:
            data = self.domain_model.get_paginated_data(raw_data)
        except Exception:  # TODO
            raise
        return data


class AuthorDetail(LiteratureDetail):
    """
    $ curl 127.0.0.1:8000/api/authors/1607170/?fields-include=name,deleted
    """
    #domain_model_class = AuthorDetailDomain
    pid_type = 'aut'


class AuthorsList(QueryParamsParserMixin, generics.ListAPIView):
    """
    $ curl "127.0.0.1:8000/api/authors/?literature=335152&fields-include=name,ids"
    $ curl "127.0.0.1:8000/api/authors/?orcid=0000-1234-...&fields-include=name,ids"
    """
    serializer_class = serializers.RecordMetadataSerializer
    domain_model_class = AuthorsListDomain

    def get_queryset(self, *args, **kwargs):
        self.domain_model = self.domain_model_class(
            query_params_parser=self.query_params_parser
        )
        return self.domain_model.get_queryset()

    def paginate_queryset(self, *args, **kwargs):
        raw_data = super().paginate_queryset(*args, **kwargs)
        try:
            data = self.domain_model.get_paginated_data(raw_data)
        except Exception:  # TODO
            raise
        return data


class OrcidIdentityDetail(QueryParamsParserMixin, generics.RetrieveAPIView):
    """
    $ curl 127.0.0.1:8000/api/identities/orcid/0000-1234-.../?fields-extra=token,author
    # TODO: TESTS for author (fields-extra)
    """
    serializer_class = serializers.OrcidIdentitySerializer
    domain_model_class = OrcidIdentityDetailDomain

    def retrieve(self, request, *args, **kwargs):
        domain = self.domain_model_class(
            orcid_value=self.kwargs['orcid_value'],
            query_params_parser=self.query_params_parser
        )
        try:
            data = domain.get_data()
        except domain_exceptions.OrcidIdentityDoesNotExist:
            raise NotFound
        serializer = self.get_serializer(
            data, fields_extra=self.query_params_parser.fields_extra)
        return Response(serializer.data)


class OrcidIdentitiesList(QueryParamsParserMixin, generics.ListAPIView):
    """
    $ curl "127.0.0.1:8000/api/identities/orcid/?author=1039812&push=true&fields-extra=tokens"
    $ curl "127.0.0.1:8000/api/identities/orcid/?literature=1126991&push=true&fields-extra=token"
    """
    domain_model_class = OrcidIdentitiesListDomain

    def get_serializer_class(self):
        if self.query_params_parser.token_field_extra:
            return serializers.OrcidIdentityPlusTokenSerializer
        return serializers.OrcidIdentitySerializer

    def get_queryset(self, *args, **kwargs):
        self.domain_model = self.domain_model_class(
            query_params_parser=self.query_params_parser
        )
        return self.domain_model.get_queryset()
