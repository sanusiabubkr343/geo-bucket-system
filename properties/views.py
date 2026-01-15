from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from core.common.pagination import CustomBucketPagination
from .filters import PropertiesFilter
from .models import Property
from .schemas import PARAMETERS
from .serializers import PropertySerializer, PropertySearchSerializer
from .services.location_matcher import normalize_location_name
from geo.models import GeoBucket


@extend_schema_view(
  nearby_properties=PARAMETERS
)
class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing properties with auto geo-bucket assignment
    """
    queryset = Property.objects.all().select_related('geo_bucket')
    serializer_class = PropertySerializer
    pagination_class = CustomBucketPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertiesFilter
    ordering_fields = ["created_at", "updated_at"]
    http_method_names = ['get', 'post']



    @action(detail=False, methods=['get'], url_path='nearby')
    def nearby_properties(self, request):
        """
        Find properties near a given location (radius search)
        GET /api/properties/nearby/?lat=6.4698&lng=3.6285&radius=5000
        """
        try:
            lat = float(request.query_params.get('lat'))
            lng = float(request.query_params.get('lng'))
            radius = float(request.query_params.get('radius', 5000))  # Default 5km
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid lat, lng, or radius parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        point = Point(lng, lat, srid=4326)

        queryset = self.get_queryset().filter(
            location__distance_lte=(point, radius)
        ).annotate(
            distance=Distance('location', point)
        ).order_by('distance')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'center': {'lat': lat, 'lng': lng},
                'radius_meters': radius,
                'results': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='similar')
    def similar_properties(self, request, pk=None):
        """
        Find properties similar to the current one (same geo-bucket)
        GET /api/properties/{id}/similar/
        """
        property_obj = self.get_object()

        # Get properties in the same geo-bucket, excluding current
        queryset = self.get_queryset().filter(
            geo_bucket=property_obj.geo_bucket
        ).exclude(id=property_obj.id)

        # Optionally filter by price range (±20%)
        price_variance = float(request.query_params.get('price_variance', 0.2))
        min_price = property_obj.price * (1 - price_variance)
        max_price = property_obj.price * (1 + price_variance)

        queryset = queryset.filter(
            price__gte=min_price,
            price__lte=max_price
        ).order_by('price')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)