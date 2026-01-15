from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

PARAMETERS = extend_schema(

    parameters=[
        OpenApiParameter(
            name="lat",
            description="Latitude of the center point",
            required=True,
            type=OpenApiTypes.NUMBER,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    'Example 1',
                    summary='Sangotedo latitude',
                    value=6.4698
                ),
                OpenApiExample(
                    'Example 2',
                    summary='Ikeja latitude',
                    value=6.6018
                ),
            ]
        ),
        OpenApiParameter(
            name="lng",
            description="Longitude of the center point",
            required=True,
            type=OpenApiTypes.NUMBER,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    'Example 1',
                    summary='Sangotedo longitude',
                    value=3.6285
                ),
                OpenApiExample(
                    'Example 2',
                    summary='Ikeja longitude',
                    value=3.3515
                ),
            ]
        ),
        OpenApiParameter(
            name="radius",
            description="Search radius in meters (default: 5000)",
            required=False,
            type=OpenApiTypes.NUMBER,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    'Default',
                    summary='5km radius',
                    value=5000
                ),
                OpenApiExample(
                    'Small',
                    summary='1km radius',
                    value=1000
                ),
                OpenApiExample(
                    'Large',
                    summary='10km radius',
                    value=10000
                ),
            ]
        ),
    ]
)