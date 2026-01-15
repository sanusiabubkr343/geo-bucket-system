from django.db.models import Count, Avg, Min, Max
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from core.common.pagination import CustomBucketPagination
from .models import GeoBucket
from .serializers import GeoBucketSerializer, BucketStatsSerializer, BucketDetailSerializer




class GeoBucketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing geo-buckets
    """
    queryset = GeoBucket.objects.all().annotate(
        property_count=Count('properties')
    ).order_by('-created_at')
    serializer_class = GeoBucketSerializer
    pagination_class = CustomBucketPagination
    http_method_names = ['get', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BucketDetailSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='stats')
    def bucket_statistics(self, request):
        """
        Get statistics about geo-buckets
        GET /api/geo-buckets/stats/
        """
        # Get all buckets with property count
        buckets = GeoBucket.objects.annotate(
            property_count=Count('properties'),
            avg_price=Avg('properties__price'),
            min_price=Min('properties__price'),
            max_price=Max('properties__price'),
            total_bedrooms=Count('properties__bedrooms')
        ).order_by('-property_count')

        # Calculate overall statistics
        total_buckets = buckets.count()
        total_properties = sum(bucket.property_count for bucket in buckets)
        avg_properties = total_properties / total_buckets if total_buckets > 0 else 0

        # Find buckets with most/least properties
        most_populated = buckets.first()
        least_populated = buckets.last() if buckets.exists() else None

        # Calculate coverage efficiency
        # (Buckets with > threshold properties vs total buckets)
        efficient_threshold = 5
        efficient_buckets = buckets.filter(property_count__gte=efficient_threshold).count()
        efficiency_rate = (efficient_buckets / total_buckets * 100) if total_buckets > 0 else 0

        # Prepare bucket details
        bucket_details = []
        for bucket in buckets:
            bucket_details.append({
                'id': bucket.id,
                'name': bucket.name,
                'normalized_name': bucket.normalized_name,
                'property_count': bucket.property_count,
                'price_stats': {
                    'avg': float(bucket.avg_price) if bucket.avg_price else 0,
                    'min': float(bucket.min_price) if bucket.min_price else 0,
                    'max': float(bucket.max_price) if bucket.max_price else 0
                },
                'center': {
                    'lat': bucket.center.y,
                    'lng': bucket.center.x
                } if bucket.center else None,
                'radius_meters': bucket.radius_meters,
                'created_at': bucket.created_at
            })

        stats_data = {
            'total_buckets': total_buckets,
            'total_properties': total_properties,
            'avg_properties_per_bucket': round(avg_properties, 2),
            'efficiency_metrics': {
                'efficient_buckets_threshold': efficient_threshold,
                'efficient_buckets_count': efficient_buckets,
                'efficiency_rate_percent': round(efficiency_rate, 1)
            },
            'extreme_buckets': {
                'most_populated': {
                    'id': most_populated.id if most_populated else None,
                    'name': most_populated.name if most_populated else None,
                    'property_count': most_populated.property_count if most_populated else 0
                },
                'least_populated': {
                    'id': least_populated.id if least_populated else None,
                    'name': least_populated.name if least_populated else None,
                    'property_count': least_populated.property_count if least_populated else 0
                }
            },
            'buckets': bucket_details
        }

        serializer = BucketStatsSerializer(data=stats_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='properties')
    def bucket_properties(self, request, pk=None):
        """
        Get all properties in a specific geo-bucket
        GET /api/geo-buckets/{id}/properties/
        """
        bucket = self.get_object()

        # Get properties in this bucket with pagination
        properties = bucket.properties.all()

        # Apply pagination
        page = self.paginate_queryset(properties)
        if page is not None:
            from properties.serializers import PropertySerializer
            serializer = PropertySerializer(page, many=True)
            return self.get_paginated_response({
                'bucket_id': bucket.id,
                'bucket_name': bucket.name,
                'results': serializer.data
            })

        from properties.serializers import PropertySerializer
        serializer = PropertySerializer(properties, many=True)
        return Response({
            'bucket_id': bucket.id,
            'bucket_name': bucket.name,
            'results': serializer.data
        })

    @action(detail=True, methods=['get'], url_path='similar')
    def similar_buckets(self, request, pk=None):
        """
        Find similar geo-buckets (by name or proximity)
        GET /api/geo-buckets/{id}/similar/
        """
        bucket = self.get_object()

        from properties.services.location_matcher import similarity

        # Find buckets with similar names
        similar_by_name = []
        all_buckets = GeoBucket.objects.exclude(id=bucket.id)

        for other_bucket in all_buckets:
            name_similarity = similarity(
                bucket.normalized_name,
                other_bucket.normalized_name
            )

            if name_similarity >= 0.7:  # 70% similarity threshold
                similar_by_name.append({
                    'bucket': other_bucket,
                    'similarity_score': name_similarity,
                    'reason': 'name_similarity'
                })

        # Find buckets nearby (within 2x radius)
        nearby_buckets = []
        if bucket.center:
            for other_bucket in all_buckets:
                if other_bucket.center:
                    distance = bucket.center.distance(other_bucket.center)
                    if distance <= bucket.radius_meters * 2:
                        nearby_buckets.append({
                            'bucket': other_bucket,
                            'distance_meters': distance.m,
                            'reason': 'proximity'
                        })

        # Combine and sort results
        similar_buckets = []

        for item in similar_by_name:
            similar_buckets.append({
                'id': item['bucket'].id,
                'name': item['bucket'].name,
                'normalized_name': item['bucket'].normalized_name,
                'property_count': item['bucket'].properties.count(),
                'reason': item['reason'],
                'score': item['similarity_score'],
                'center': {
                    'lat': item['bucket'].center.y,
                    'lng': item['bucket'].center.x
                } if item['bucket'].center else None
            })

        for item in nearby_buckets:
            similar_buckets.append({
                'id': item['bucket'].id,
                'name': item['bucket'].name,
                'normalized_name': item['bucket'].normalized_name,
                'property_count': item['bucket'].properties.count(),
                'reason': item['reason'],
                'distance_meters': round(item['distance_meters']),
                'center': {
                    'lat': item['bucket'].center.y,
                    'lng': item['bucket'].center.x
                } if item['bucket'].center else None
            })

        # Remove duplicates by id
        seen_ids = set()
        unique_similar = []
        for bucket_info in similar_buckets:
            if bucket_info['id'] not in seen_ids:
                seen_ids.add(bucket_info['id'])
                unique_similar.append(bucket_info)

        # Sort by relevance (higher score first, then closer distance)
        unique_similar.sort(key=lambda x: (
            -x.get('score', 0),
            x.get('distance_meters', float('inf'))
        ))

        return Response({
            'current_bucket': {
                'id': bucket.id,
                'name': bucket.name,
                'normalized_name': bucket.normalized_name
            },
            'similar_buckets_count': len(unique_similar),
            'similar_buckets': unique_similar
        })