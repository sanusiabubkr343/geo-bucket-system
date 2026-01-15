from django.db.models import Count, Avg, Min, Max
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from core.common.pagination import CustomBucketPagination
from .models import GeoBucket
from .schemas import GEO_PARAMETERS
from .serializers import GeoBucketSerializer, BucketStatsSerializer, BucketDetailSerializer
from .utils import calculate_bucket_statistics


@extend_schema_view(
  bucket_statistics=GEO_PARAMETERS
)
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
        Get comprehensive statistics about geo-buckets
        GET /api/geo-buckets/stats/
        """
        # Get query parameters
        time_period = request.query_params.get('time_period')
        include_buckets = request.query_params.get('include_buckets', 'true').lower() == 'true'
        limit = int(request.query_params.get('limit', 50))

        try:
            stats_data = calculate_bucket_statistics(time_period)

            if not include_buckets:
                stats_data['buckets'] = []
            else:
                # Limit bucket details
                stats_data['buckets'] = stats_data['buckets'][:limit]

            # Serialize response
            serializer = BucketStatsSerializer(data=stats_data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Failed to calculate statistics: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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

