from rest_framework import serializers

from .db_models.inspirehep import RecordMetadata, UserIdentity

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy

class RecordMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordMetadata
        fields = '__all__'


class UserIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdentity
        fields = '__all__'
