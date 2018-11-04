from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from rest_framework import mixins, generics, permissions, viewsets, renderers, views
from rest_framework.decorators import api_view, detail_route
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import serializers
from .domain_models.record_metadata_base import RecordMetadataDetailDomainBase
from .domain_models.authors import AuthorsListDomain
from .domain_models.orcids import OrcidIdentitiesListDomain
from .domain_models import exceptions as domain_exceptions


def health(request):
    now = timezone.localtime(timezone.now())
    return JsonResponse({'date': now})


def unhealth(request):
    class UnhealthTestException(Exception):
        pass

    now = timezone.localtime(timezone.now())
    raise UnhealthTestException('/unhealth endpoint called on {}'.format(now))
    return 'It should have raised UnhealthTestException'


class LiteratureDetail(generics.RetrieveAPIView):
    """
    $ curl 127.0.0.1:8000/api/literature/335152/?fields-include=titles,control_number

    Tests
    """
    serializer_class = serializers.RecordMetadataSerializer
    domain_model_class = RecordMetadataDetailDomainBase
    pid_type = 'lit'

    def retrieve(self, request, *args, **kwargs):
        domain = self.domain_model_class(
            pid_type=self.pid_type,
            pid_value=self.kwargs['pid_value'],
            query_params=request.query_params
        )
        try:
            data = domain.get_data()
        except domain_exceptions.RecordMetadataDoesNotExist:
            raise NotFound
        serializer = self.get_serializer(data)
        return Response(serializer.data)


# TODO
# class LiteratureList(generics.ListAPIView):
#     """
#     $ curl "127.0.0.1:8000/api/literature/?author=1607170&fields-include=titles"
#     *** HARD  $ curl "127.0.0.1:8000/api/literature/?author-orcidiidentity=xxxxxx&push=true&fields-include=titles"
#     """

class AuthorDetail(LiteratureDetail):
    """
    $ curl 127.0.0.1:8000/api/authors/1607170/?fields-include=name,deleted
    """
    #domain_model_class = AuthorDetailDomain
    pid_type = 'aut'


# TODO: manage records_metadata.json['deleted'] == True?


class AuthorsList(generics.ListAPIView):
    """
    $ curl "127.0.0.1:8000/api/authors/?literature=335152&fields-include=name,ids"
    """
    serializer_class = serializers.RecordMetadataSerializer
    domain_model_class = AuthorsListDomain

    def get_queryset(self, *args, **kwargs):
        self.domain_model = self.domain_model_class(
            query_params=self.request.query_params
        )
        return self.domain_model.get_queryset()

    def paginate_queryset(self, *args, **kwargs):
        raw_data = super().paginate_queryset(*args, **kwargs)
        try:
            data = self.domain_model.get_paginated_data(raw_data)
        except Exception:
            raise
        return data


class OrcidIdentitiesList(generics.ListAPIView):
    """
    $ curl "127.0.0.1:8000/api/identities/orcid/?author=1039812&push=true&fields-extra=tokens"
    $ curl "127.0.0.1:8000/api/identities/orcid/?literature=1126991&push=true&fields-extra=tokens"
    TODO:
     - push=true
     - author=xxxx
     - fields-extra=tokens
    """
    serializer_class = serializers.OrcidIdentitySerializer
    domain_model_class = OrcidIdentitiesListDomain

    def get_queryset(self, *args, **kwargs):
        self.domain_model = self.domain_model_class(
            query_params=self.request.query_params
        )
        return self.domain_model.get_queryset()


