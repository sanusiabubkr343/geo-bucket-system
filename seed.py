#!/usr/bin/env python
"""
Geo Bucket System - Sample Data Seed Script (Python Version)
Run with: python manage.py shell < seed.py
"""

import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.gis.geos import Point
from django.utils import timezone
from geo.models import GeoBucket
from properties.models import Property


def clear_data():
    """Clear existing data"""
    print("Clearing existing data...")
    Property.objects.all().delete()
    GeoBucket.objects.all().delete()
    print("Data cleared.")


def create_geo_buckets():
    """Create sample geo buckets"""
    print("Creating geo buckets...")

    buckets_data = [
        # Sangotedo Area
        {'name': 'Sangotedo', 'normalized_name': 'sangotedo', 'lat': 6.4698, 'lng': 3.6285},
        {'name': 'Sangotedo Phase 1', 'normalized_name': 'sangotedo phase 1', 'lat': 6.4710, 'lng': 3.6300},
        {'name': 'Sangotedo Estate', 'normalized_name': 'sangotedo estate', 'lat': 6.4685, 'lng': 3.6270},

        # Ikeja Area
        {'name': 'Ikeja GRA', 'normalized_name': 'ikeja gra', 'lat': 6.6018, 'lng': 3.3515},
        {'name': 'Ikeja CBD', 'normalized_name': 'ikeja cbd', 'lat': 6.6025, 'lng': 3.3500},
        {'name': 'Ikeja', 'normalized_name': 'ikeja', 'lat': 6.6030, 'lng': 3.3490},

        # Lekki Area
        {'name': 'Lekki Phase 1', 'normalized_name': 'lekki phase 1', 'lat': 6.4442, 'lng': 3.4616},
        {'name': 'Lekki', 'normalized_name': 'lekki', 'lat': 6.4750, 'lng': 3.5780},

        # Victoria Island
        {'name': 'Victoria Island', 'normalized_name': 'victoria island', 'lat': 6.4289, 'lng': 3.4210},
        {'name': 'VI', 'normalized_name': 'vi', 'lat': 6.4275, 'lng': 3.4230},

        # Ajah Area
        {'name': 'Ajah', 'normalized_name': 'ajah', 'lat': 6.4800, 'lng': 3.6400},
        {'name': 'Ajah Lagos', 'normalized_name': 'ajah lagos', 'lat': 6.4780, 'lng': 3.6380},

        # Other Areas
        {'name': 'Surulere', 'normalized_name': 'surulere', 'lat': 6.5010, 'lng': 3.3560},
        {'name': 'Yaba', 'normalized_name': 'yaba', 'lat': 6.5150, 'lng': 3.3800},
        {'name': 'Ikoyi', 'normalized_name': 'ikoyi', 'lat': 6.4520, 'lng': 3.4350},
        {'name': 'Apapa', 'normalized_name': 'apapa', 'lat': 6.4480, 'lng': 3.3600},
        {'name': 'Maryland', 'normalized_name': 'maryland', 'lat': 6.5750, 'lng': 3.3650},
        {'name': 'Ogba', 'normalized_name': 'ogba', 'lat': 6.6200, 'lng': 3.3300},
    ]

    created_buckets = {}
    for i, data in enumerate(buckets_data, 1):
        bucket = GeoBucket.objects.create(
            name=data['name'],
            normalized_name=data['normalized_name'],
            center=Point(data['lng'], data['lat']),
            radius_meters=1000,
            created_at=timezone.now() - timedelta(days=random.randint(10, 40))
        )
        created_buckets[data['name']] = bucket
        print(f"  Created bucket: {data['name']}")

    print(f"✓ Created {len(created_buckets)} geo buckets")
    return created_buckets


def create_properties(buckets):
    """Create sample properties"""
    print("\nCreating properties...")

    properties_data = [
        # Sangotedo Area
        {'title': 'Luxury Villa Sangotedo', 'location_name': 'Sangotedo', 'bucket': 'Sangotedo',
         'lat': 6.4698, 'lng': 3.6285, 'price': 75000000, 'bedrooms': 5, 'bathrooms': 4},
        {'title': 'Modern Duplex Sangotedo', 'location_name': 'Sangotedo', 'bucket': 'Sangotedo',
         'lat': 6.4700, 'lng': 3.6290, 'price': 85000000, 'bedrooms': 6, 'bathrooms': 5},
        {'title': 'Affordable Bungalow Sangotedo', 'location_name': 'Sangotedo', 'bucket': 'Sangotedo',
         'lat': 6.4695, 'lng': 3.6280, 'price': 35000000, 'bedrooms': 3, 'bathrooms': 2},

        # Sangotedo Phase 1
        {'title': 'Phase 1 Luxury Apartment', 'location_name': 'Sangotedo Phase 1', 'bucket': 'Sangotedo Phase 1',
         'lat': 6.4712, 'lng': 3.6305, 'price': 65000000, 'bedrooms': 4, 'bathrooms': 3},
        {'title': 'Phase 1 Townhouse', 'location_name': 'Sangotedo Phase 1', 'bucket': 'Sangotedo Phase 1',
         'lat': 6.4708, 'lng': 3.6298, 'price': 55000000, 'bedrooms': 4, 'bathrooms': 3},

        # Ikeja GRA
        {'title': 'GRA Executive Duplex', 'location_name': 'Ikeja GRA', 'bucket': 'Ikeja GRA',
         'lat': 6.6020, 'lng': 3.3520, 'price': 120000000, 'bedrooms': 5, 'bathrooms': 4},
        {'title': 'GRA Mini Estate', 'location_name': 'Ikeja GRA', 'bucket': 'Ikeja GRA',
         'lat': 6.6015, 'lng': 3.3510, 'price': 180000000, 'bedrooms': 8, 'bathrooms': 6},

        # Ikeja CBD
        {'title': 'CBD Office Space', 'location_name': 'Ikeja Central Business District', 'bucket': 'Ikeja CBD',
         'lat': 6.6028, 'lng': 3.3505, 'price': 300000000, 'bedrooms': 0, 'bathrooms': 10},
        {'title': 'CBD Commercial Plaza', 'location_name': 'Ikeja CBD', 'bucket': 'Ikeja CBD',
         'lat': 6.6020, 'lng': 3.3495, 'price': 500000000, 'bedrooms': 0, 'bathrooms': 15},

        # Lekki Phase 1
        {'title': 'Lekki Waterfront Villa', 'location_name': 'Lekki Phase 1', 'bucket': 'Lekki Phase 1',
         'lat': 6.4445, 'lng': 3.4620, 'price': 280000000, 'bedrooms': 7, 'bathrooms': 6},
        {'title': 'Phase 1 Luxury Penthouse', 'location_name': 'Lekki Phase 1', 'bucket': 'Lekki Phase 1',
         'lat': 6.4438, 'lng': 3.4610, 'price': 350000000, 'bedrooms': 6, 'bathrooms': 5},

        # Victoria Island
        {'title': 'VI Luxury Penthouse', 'location_name': 'Victoria Island', 'bucket': 'Victoria Island',
         'lat': 6.4292, 'lng': 3.4215, 'price': 500000000, 'bedrooms': 5, 'bathrooms': 4},
        {'title': 'VI Executive Suite', 'location_name': 'Victoria Island Lagos', 'bucket': 'Victoria Island',
         'lat': 6.4285, 'lng': 3.4205, 'price': 320000000, 'bedrooms': 4, 'bathrooms': 3},
    ]

    # Add some variations for testing
    for i in range(10):
        bucket_name = random.choice(['Sangotedo', 'Ikeja', 'Lekki Phase 1', 'Victoria Island'])
        bucket = buckets[bucket_name]

        properties_data.append({
            'title': f'Test Property {i + 1} {bucket_name}',
            'location_name': bucket_name,
            'bucket': bucket_name,
            'lat': bucket.center.y + random.uniform(-0.001, 0.001),
            'lng': bucket.center.x + random.uniform(-0.001, 0.001),
            'price': random.randint(20000000, 150000000),
            'bedrooms': random.randint(1, 5),
            'bathrooms': random.randint(1, 4),
        })

    for data in properties_data:
        Property.objects.create(
            title=data['title'],
            location_name=data['location_name'],
            location=Point(data['lng'], data['lat']),
            price=data['price'],
            bedrooms=data['bedrooms'],
            bathrooms=data['bathrooms'],
            geo_bucket=buckets[data['bucket']],
            created_at=timezone.now() - timedelta(days=random.randint(0, 30))
        )
        print(f"  Created property: {data['title']}")

    print(f"✓ Created {len(properties_data)} properties")


def verify_data():
    """Verify the seeded data"""
    print("\n" + "=" * 50)
    print("VERIFICATION RESULTS")
    print("=" * 50)

    total_buckets = GeoBucket.objects.count()
    total_properties = Property.objects.count()

    print(f"Total Buckets: {total_buckets}")
    print(f"Total Properties: {total_properties}")

    # Check properties per bucket
    from django.db.models import Count
    bucket_stats = GeoBucket.objects.annotate(
        property_count=Count('properties')
    ).order_by('-property_count')

    print("\nTop 5 Most Populated Buckets:")
    for bucket in bucket_stats[:5]:
        print(f"  {bucket.name}: {bucket.property_count} properties")

    # Check Sangotedo grouping
    sangotedo_buckets = GeoBucket.objects.filter(normalized_name__icontains='sangotedo')
    sangotedo_properties = Property.objects.filter(geo_bucket__in=sangotedo_buckets).count()
    print(f"\nSangotedo Area:")
    print(f"  Buckets: {sangotedo_buckets.count()}")
    print(f"  Total Properties: {sangotedo_properties}")

    # Price statistics
    from django.db.models import Avg, Min, Max
    price_stats = Property.objects.aggregate(
        avg_price=Avg('price'),
        min_price=Min('price'),
        max_price=Max('price')
    )

    print(f"\nPrice Statistics:")
    print(f"  Average Price: ₦{price_stats['avg_price']:,.2f}")
    print(f"  Minimum Price: ₦{price_stats['min_price']:,.2f}")
    print(f"  Maximum Price: ₦{price_stats['max_price']:,.2f}")


def main():
    """Main seed function"""
    print("=" * 50)
    print("GEO BUCKET SYSTEM - SEED DATA SCRIPT")
    print("=" * 50)

    # Ask for confirmation
    response = input("\nThis will clear existing data. Continue? (y/N): ")
    if response.lower() != 'y':
        print("Seed cancelled.")
        return

    # Clear data
    clear_data()

    # Create buckets and properties
    buckets = create_geo_buckets()
    create_properties(buckets)

    # Verify
    verify_data()

    print("\n" + "=" * 50)
    print("✅ SEED COMPLETE!")
    print("=" * 50)
    print("\nTest the following endpoints:")
    print("1. GET /api/geo-buckets/stats/")
    print("2. GET /api/properties/search/?location=sangotedo")
    print("3. GET /api/properties/nearby/?lat=6.4698&lng=3.6285&radius=5000")
    print("\nHappy testing! 🎉")


if __name__ == "__main__":
    main()