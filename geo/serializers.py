from rest_framework import serializers

from properties.serializers import PropertySerializer
from .models import GeoBucket


class GeoBucketSerializer(serializers.ModelSerializer):
    property_count = serializers.SerializerMethodField(method_name='get_property_count')

    class Meta:
        model = GeoBucket
        fields = [
            'id', 'name', 'normalized_name', 'center',
            'radius_meters', 'property_count', 'created_at'
        ]

    def get_property_count(self, obj):
        return obj.properties.count()


class BucketStatsSerializer(serializers.Serializer):
    total_buckets = serializers.IntegerField()
    total_properties = serializers.IntegerField()
    avg_properties_per_bucket = serializers.FloatField()
    buckets = serializers.ListField(child=serializers.DictField())


class BucketDetailSerializer(GeoBucketSerializer):
    """Detailed serializer for single bucket view"""
    properties = PropertySerializer(many=True, read_only=True, source='properties.all')

    class Meta(GeoBucketSerializer.Meta):
        fields = GeoBucketSerializer.Meta.fields + ['properties']


class SimilarBucketSerializer(serializers.Serializer):
    """Serializer for similar buckets response"""
    current_bucket = serializers.DictField()
    similar_buckets_count = serializers.IntegerField()
    similar_buckets = serializers.ListField(child=serializers.DictField())