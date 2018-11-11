from rest_framework import serializers
from rest_framework.fields import ModelField

from .models.inspirehep import RecordMetadata, OrcidIdentity

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy

class RecordMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordMetadata
        fields = '__all__'


class OrcidIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcidIdentity
        fields = '__all__'


class OrcidIdentityPlusTokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = OrcidIdentity
        fields = '__all__'

    def get_token(self, model):
        # TODO display access token encrypted
        return str(model.remotetoken.access_token)
