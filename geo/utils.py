from django.db.models import Count, Avg, Min, Max, Sum
from django.db.models.functions import Round
from datetime import datetime, timedelta
from geo.models import GeoBucket


def calculate_bucket_statistics(time_period=None):
    """
    Calculate comprehensive statistics for geo-buckets

    Args:
        time_period: Optional time period filter (e.g., '7d', '30d', '90d')

    Returns:
        dict: Complete statistics data
    """
    # Apply time filter if specified
    queryset = GeoBucket.objects.all()

    if time_period:
        days = int(time_period.rstrip('d'))
        cutoff_date = datetime.now() - timedelta(days=days)
        queryset = queryset.filter(created_at__gte=cutoff_date)

    # Annotate buckets with statistics
    buckets = queryset.annotate(
        property_count=Count('properties'),
        avg_price=Avg('properties__price'),
        min_price=Min('properties__price'),
        max_price=Max('properties__price'),
        total_value=Sum('properties__price'),
        total_bedrooms=Sum('properties__bedrooms'),
        total_bathrooms=Sum('properties__bathrooms')
    ).order_by('-property_count')

    # Calculate overall statistics
    total_buckets = buckets.count()
    total_properties = sum(bucket.property_count for bucket in buckets)
    avg_properties = total_properties / total_buckets if total_buckets > 0 else 0

    # Calculate coverage efficiency with multiple thresholds
    efficiency_thresholds = [
        {'threshold': 1, 'label': 'Used Buckets'},
        {'threshold': 5, 'label': 'Well-Used Buckets'},
        {'threshold': 10, 'label': 'Highly Active Buckets'}
    ]

    efficiency_metrics = []
    for threshold_config in efficiency_thresholds:
        threshold = threshold_config['threshold']
        label = threshold_config['label']

        efficient_count = buckets.filter(property_count__gte=threshold).count()
        efficiency_rate = (efficient_count / total_buckets * 100) if total_buckets > 0 else 0

        efficiency_metrics.append({
            'label': label,
            'threshold': threshold,
            'count': efficient_count,
            'percentage': round(efficiency_rate, 1)
        })

    # Find extreme buckets
    most_populated = buckets.first()
    least_populated = buckets.filter(property_count__gt=0).last() if buckets.filter(
        property_count__gt=0).exists() else None

    # Calculate property distribution
    property_distribution = {
        'empty_buckets': buckets.filter(property_count=0).count(),
        'single_property': buckets.filter(property_count=1).count(),
        'few_properties': buckets.filter(property_count__range=(2, 5)).count(),
        'many_properties': buckets.filter(property_count__gte=6).count(),
    }

    # Calculate value statistics
    total_value = sum(bucket.total_value or 0 for bucket in buckets)
    avg_value_per_bucket = total_value / total_buckets if total_buckets > 0 else 0

    # Prepare bucket details (limit to top buckets for performance)
    bucket_details = []
    for bucket in buckets[:50]:  # Limit to top 50 buckets
        bucket_details.append({
            'id': bucket.id,
            'name': bucket.name,
            'normalized_name': bucket.normalized_name,
            'property_count': bucket.property_count,
            'property_stats': {
                'avg_price': float(bucket.avg_price) if bucket.avg_price else 0,
                'min_price': float(bucket.min_price) if bucket.min_price else 0,
                'max_price': float(bucket.max_price) if bucket.max_price else 0,
                'total_value': float(bucket.total_value) if bucket.total_value else 0,
                'total_bedrooms': bucket.total_bedrooms or 0,
                'total_bathrooms': bucket.total_bathrooms or 0,
            },
            'center': {
                'lat': bucket.center.y if bucket.center else None,
                'lng': bucket.center.x if bucket.center else None
            },
            'radius_meters': bucket.radius_meters,
            'created_at': bucket.created_at.isoformat() if bucket.created_at else None,
            'density': bucket.property_count / (
                        3.14 * (bucket.radius_meters / 1000) ** 2) if bucket.radius_meters > 0 else 0
        })

    # Calculate coverage metrics
    if buckets.filter(property_count__gt=0).exists():
        avg_radius = buckets.filter(property_count__gt=0).aggregate(
            avg_radius=Avg('radius_meters')
        )['avg_radius'] or 0

        # Estimate coverage area (simplified)
        coverage_area = sum(
            3.14 * (bucket.radius_meters / 1000) ** 2
            for bucket in buckets.filter(property_count__gt=0)
        )
    else:
        avg_radius = 0
        coverage_area = 0

    return {
        'summary': {
            'total_buckets': total_buckets,
            'total_properties': total_properties,
            'total_value': round(total_value, 2),
            'avg_properties_per_bucket': round(avg_properties, 2),
            'avg_value_per_bucket': round(avg_value_per_bucket, 2),
            'property_distribution': property_distribution,
        },
        'efficiency_metrics': efficiency_metrics,
        'coverage_metrics': {
            'avg_bucket_radius_meters': round(avg_radius, 2),
            'estimated_coverage_area_sq_km': round(coverage_area, 2),
            'buckets_with_properties': buckets.filter(property_count__gt=0).count(),
        },
        'extreme_buckets': {
            'most_populated': {
                'id': most_populated.id if most_populated else None,
                'name': most_populated.name if most_populated else None,
                'property_count': most_populated.property_count if most_populated else 0,
                'total_value': float(
                    most_populated.total_value) if most_populated and most_populated.total_value else 0,
            } if most_populated else None,
            'least_populated': {
                'id': least_populated.id if least_populated else None,
                'name': least_populated.name if least_populated else None,
                'property_count': least_populated.property_count if least_populated else 0,
            } if least_populated else None,
            'highest_value': {
                'id': max(buckets, key=lambda x: x.total_value or 0).id if buckets.exists() else None,
                'total_value': float(
                    max(buckets, key=lambda x: x.total_value or 0).total_value) if buckets.exists() else 0,
            } if buckets.exists() else None,
        },
        'buckets': bucket_details,
        'time_period': time_period,
        'timestamp': datetime.now().isoformat()
    }