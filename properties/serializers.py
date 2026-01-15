from rest_framework import serializers
from .models import Property
from .services.geo_bucket import find_or_create_bucket_improved


class PropertySerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(write_only=True)
    lng = serializers.FloatField(write_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'location_name', 'lat', 'lng',
            'price', 'bedrooms', 'bathrooms', 'geo_bucket', 'created_at'
        ]
        read_only_fields = ['geo_bucket', 'created_at']


    def validate(self, attrs):
        lat = attrs['lat']
        lng = attrs['lng']

        if lat < -90 or lat > 90:
            raise serializers.ValidationError('Latitude must be between -90 and 90')
        if lng < -180 or lng > 180:
            raise serializers.ValidationError('Longitude must be between -180 and 180')
        return attrs


    def create(self, validated_data):
        lat = validated_data.pop('lat')
        lng = validated_data.pop('lng')

        # Create bucket or find existing
        geo_bucket = find_or_create_bucket_improved(
            location_name=validated_data['location_name'],
            lat=lat,
            lng=lng
        )

        property_obj = Property.objects.create(
            **validated_data,
            location=f"POINT({lng} {lat})",
            geo_bucket=geo_bucket
        )

        return property_obj



class PropertySearchSerializer(serializers.Serializer):
    """Serializer for search results metadata"""
    search_type = serializers.CharField()
    normalized_query = serializers.CharField(required=False)
    matching_buckets_count = serializers.IntegerField(required=False)
    center = serializers.DictField(required=False)
    radius_meters = serializers.FloatField(required=False)
    results = PropertySerializer(many=True)