from rest_framework import serializers

from .db_models.inspirehep import RecordMetadata

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy

# class RecordMetadataSerializer(serializers.Serializer):
class RecordMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordMetadata
        fields = '__all__'
