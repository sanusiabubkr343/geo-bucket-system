
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from geo.models import GeoBucket
from properties.services.location_matcher import normalize_location_name, similarity

BUCKET_RADIUS_METERS = 1000
SIMILARITY_THRESHOLD = 0.3


def find_or_create_bucket_improved(location_name: str, lat: float, lng: float) -> GeoBucket:
    normalized = normalize_location_name(location_name)
    point = Point(lng, lat)

    print(f"DEBUG: Location: {location_name}")
    print(f"DEBUG: Normalized: {normalized}")
    print(f"DEBUG: Point: {point}")

    # 1. Try exact match first
    exact_match = GeoBucket.objects.filter(
        normalized_name=normalized,
        center__distance_lte=(point, D(m=BUCKET_RADIUS_METERS))
    ).first()

    print(f"DEBUG: Exact matches found: {exact_match}")

    # 2. Try fuzzy match
    nearby_buckets = GeoBucket.objects.filter(
        center__distance_lte=(point, D(m=BUCKET_RADIUS_METERS * 1.5))
    )

    print(f"DEBUG: Nearby buckets count: {nearby_buckets.count()}")

    for bucket in nearby_buckets:
        sim = similarity(bucket.normalized_name, normalized)
        print(f"DEBUG: Comparing '{bucket.normalized_name}' with '{normalized}': {sim}")
        if sim >= SIMILARITY_THRESHOLD:
            print(f"DEBUG: Found match! Similarity: {sim}")
            return bucket

    print(f"DEBUG: Creating new bucket")
    return GeoBucket.objects.create(
        name=location_name,
        normalized_name=normalized,
        center=point,
        radius_meters=BUCKET_RADIUS_METERS,
    )