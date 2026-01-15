from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from core.common.pagination import CustomBucketPagination
from .filters import PropertiesFilter
from .models import Property
from .serializers import PropertySerializer, PropertySearchSerializer
from .services.location_matcher import normalize_location_name
from geo.models import GeoBucket



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

    def create(self, request, *args, **kwargs):
        """
        Override create to handle lat/lng extraction and geo-bucket assignment
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create property (serializer handles geo-bucket assignment)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['get'], url_path='search')
    def search_by_location(self, request):
        """
        Search properties by location with typo-tolerance
        GET /api/properties/search/?location=sangotedo
        """
        location_query = request.query_params.get('location', '').strip()
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', 5000)  # Default 5km

        if not location_query and not (lat and lng):
            return Response(
                {"error": "Either 'location' parameter or 'lat' and 'lng' parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset()

        # If lat/lng provided, do radius search
        if lat and lng:
            try:
                point = Point(float(lng), float(lat), srid=4326)
                radius_float = float(radius)

                queryset = queryset.filter(
                    location__distance_lte=(point, radius_float)
                ).annotate(
                    distance=Distance('location', point)
                ).order_by('distance')

                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response({
                        'search_type': 'radius',
                        'center': {'lat': lat, 'lng': lng},
                        'radius_meters': radius,
                        'results': serializer.data
                    })

            except (ValueError, TypeError) as e:
                return Response(
                    {"error": f"Invalid coordinates or radius: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Location-based search with fuzzy matching
        normalized_query = normalize_location_name(location_query)

        # Get matching geo-buckets using fuzzy matching
        from properties.services.location_matcher import similarity

        all_buckets = GeoBucket.objects.all()
        matching_bucket_ids = []

        for bucket in all_buckets:
            # Check similarity with normalized bucket name
            if similarity(bucket.normalized_name, normalized_query) >= 0.6:
                matching_bucket_ids.append(bucket.id)
            # Also check similarity with original name
            elif similarity(bucket.name.lower(), location_query.lower()) >= 0.6:
                matching_bucket_ids.append(bucket.id)

        # Search in properties
        if matching_bucket_ids:
            queryset = queryset.filter(geo_bucket_id__in=matching_bucket_ids)
        else:
            # Fallback: search in location names with some tolerance
            queryset = queryset.filter(
                Q(location_name__icontains=normalized_query.split()[0]) |  # First word
                Q(geo_bucket__normalized_name__icontains=normalized_query.split()[0])
            )

        # Apply filters if provided
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        min_bedrooms = request.query_params.get('min_bedrooms')
        max_bedrooms = request.query_params.get('max_bedrooms')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_bedrooms:
            queryset = queryset.filter(bedrooms__gte=min_bedrooms)
        if max_bedrooms:
            queryset = queryset.filter(bedrooms__lte=max_bedrooms)

        # Order results
        order_by = request.query_params.get('order_by', '-created_at')
        if order_by.lstrip('-') in ['price', 'bedrooms', 'bathrooms', 'created_at']:
            queryset = queryset.order_by(order_by)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'search_type': 'location',
                'normalized_query': normalized_query,
                'matching_buckets_count': len(matching_bucket_ids),
                'results': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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