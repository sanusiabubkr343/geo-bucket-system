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
    """Serializer for bucket statistics response"""

    # Summary section
    summary = serializers.DictField()

    # Efficiency metrics
    efficiency_metrics = serializers.ListField(
        child=serializers.DictField()
    )

    # Coverage metrics
    coverage_metrics = serializers.DictField()

    # Extreme buckets
    extreme_buckets = serializers.DictField()

    # Bucket details
    buckets = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )

    # Metadata
    time_period = serializers.CharField(
        required=False,
        allow_null=True
    )
    timestamp = serializers.DateTimeField()

    class Meta:
        fields = [
            'summary', 'efficiency_metrics', 'coverage_metrics',
            'extreme_buckets', 'buckets', 'time_period', 'timestamp'
        ]

class BucketDetailSerializer(GeoBucketSerializer):
    """Detailed serializer for single bucket view"""
    properties = PropertySerializer(many=True, read_only=True, source='properties.all')

    class Meta(GeoBucketSerializer.Meta):
        fields = GeoBucketSerializer.Meta.fields + ['properties']


