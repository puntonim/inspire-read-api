from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models.inspirehep import RecordMetadata, OrcidIdentity

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy

class RecordMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordMetadata
        fields = '__all__'


class OrcidIdentitySerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    author_pid = serializers.SerializerMethodField()

    class Meta:
        model = OrcidIdentity
        fields = '__all__'

    def __init__(self, *args, fields_extra=None, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO move this to a mixin
        if 'token' not in fields_extra:
            del self.fields['token']
        if 'author' not in fields_extra:
            del self.fields['author_pid']

    def get_token(self, model):
        try:
            return model.remote_token.access_token_plain
        except ObjectDoesNotExist:
            return None

    def get_author_pid(self, model):
        try:
            return model.author_pid
        except ObjectDoesNotExist:
            return None
