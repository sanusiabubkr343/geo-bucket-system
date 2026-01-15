
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from geo.models import GeoBucket
from properties.services.location_matcher import normalize_location_name, similarity

BUCKET_RADIUS_METERS = 1000
SIMILARITY_THRESHOLD = 0.8


def find_or_create_bucket_improved(location_name: str, lat: float, lng: float) -> GeoBucket:
    normalized = normalize_location_name(location_name)
    point = Point(lng, lat)

    # 1. Try exact match first (fastest)
    exact_match = GeoBucket.objects.filter(
        normalized_name=normalized,
        center__distance_lte=(point, D(m=BUCKET_RADIUS_METERS))
    ).first()

    if exact_match:
        return exact_match

    # 2. Try fuzzy match on pre-filtered set
    nearby_buckets = GeoBucket.objects.filter(
        center__distance_lte=(point, D(m=BUCKET_RADIUS_METERS * 1.5))  # Slightly larger radius
    )

    for bucket in nearby_buckets:
        if similarity(bucket.normalized_name, normalized) >= SIMILARITY_THRESHOLD:
            return bucket

    # 3. Create new
    return GeoBucket.objects.create(
        name=location_name,
        normalized_name=normalized,
        center=point,
        radius_meters=BUCKET_RADIUS_METERS,
    )