from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


GEO_PARAMETERS=extend_schema(
    parameters=[
        OpenApiParameter(
            name="time_period",
            description="Filter statistics by time period (e.g., 7d, 30d, 90d)",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    'Last 7 days',
                    value='7d'
                ),
                OpenApiExample(
                    'Last 30 days',
                    value='30d'
                ),
                OpenApiExample(
                    'Last 90 days',
                    value='90d'
                ),
            ]
        ),
        OpenApiParameter(
            name="include_buckets",
            description="Include detailed bucket list in response",
            required=False,
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            default=True
        ),
        OpenApiParameter(
            name="limit",
            description="Limit the number of buckets in response",
            required=False,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            default=50
        ),
    ],
    description="""
    Get comprehensive statistics about geo-buckets

    Returns:
    - Total buckets and properties
    - Properties per bucket distribution
    - Coverage and efficiency metrics
    - Top performing buckets
    - Time-based analytics (if time_period provided)
    """,
    examples=[
        OpenApiExample(
            'Success Response',
            summary='Complete bucket statistics',
            value={
                'summary': {
                    'total_buckets': 25,
                    'total_properties': 150,
                    'total_value': 4500000000,
                    'avg_properties_per_bucket': 6.0,
                    'avg_value_per_bucket': 180000000,
                    'property_distribution': {
                        'empty_buckets': 5,
                        'single_property': 3,
                        'few_properties': 10,
                        'many_properties': 7
                    }
                },
                'efficiency_metrics': [
                    {
                        'label': 'Used Buckets',
                        'threshold': 1,
                        'count': 20,
                        'percentage': 80.0
                    },
                    {
                        'label': 'Well-Used Buckets',
                        'threshold': 5,
                        'count': 12,
                        'percentage': 48.0
                    },
                    {
                        'label': 'Highly Active Buckets',
                        'threshold': 10,
                        'count': 5,
                        'percentage': 20.0
                    }
                ],
                'coverage_metrics': {
                    'avg_bucket_radius_meters': 1000.0,
                    'estimated_coverage_area_sq_km': 78.5,
                    'buckets_with_properties': 20
                },
                'extreme_buckets': {
                    'most_populated': {
                        'id': 1,
                        'name': 'Sangotedo',
                        'property_count': 45,
                        'total_value': 1350000000
                    },
                    'least_populated': {
                        'id': 23,
                        'name': 'Victoria Island',
                        'property_count': 1
                    }
                },
                'timestamp': '2024-01-15T10:30:00Z'
            },
            response_only=True
        )
    ]
)






