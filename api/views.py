from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from rest_framework import mixins, generics, permissions, viewsets, renderers, views
from rest_framework.decorators import api_view, detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import serializers
from .db_models.inspirehep import RecordMetadata
from .domain_models.literature import LiteratureDetailDomain
from .domain_models.authors import AuthorDetailDomain, AuthorsListDomain
from .domain_models.orcids import OrcidIdentitiesListDomain


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
    """
    serializer_class = serializers.RecordMetadataSerializer
    domain_model_class = LiteratureDetailDomain

    def retrieve(self, request, *args, **kwargs):
        domain = self.domain_model_class(
            pid_value=self.kwargs['pid_value'],
            query_params=request.query_params
        )
        try:
            data = domain.get_data()
        except Exception:  # TODO catch domains exceptions
            raise
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
    domain_model_class = AuthorDetailDomain


# TODO: manage records_metadata.json['deleted'] == True?


class AuthorsList(generics.ListAPIView):
    """
    $ curl "127.0.0.1:8000/api/authors/?literature=335152&fields-include=name"
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
    $ curl "127.0.0.1:8000/api/identities/orcid/?author=1039812&push=true"
    $ curl "127.0.0.1:8000/api/identities/orcid/?literature=1126991&push=true"
    TODO:
     - push=true
     - author
    """
    serializer_class = serializers.UserIdentitySerializer
    domain_model_class = OrcidIdentitiesListDomain

    def get_queryset(self, *args, **kwargs):
        self.domain_model = self.domain_model_class(
            query_params=self.request.query_params
        )
        return self.domain_model.get_queryset()


