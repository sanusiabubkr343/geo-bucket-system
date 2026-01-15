import pytest
import os
import django
from django.contrib.gis.geos import Point
from datetime import datetime, timedelta
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from geo.models import GeoBucket
from properties.models import Property


@pytest.fixture
def api_client():
    """API test client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_user(db):
    """Create a test user"""
    def make_user(username='testuser', password='testpass123', email='test@example.com'):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
    return make_user


@pytest.fixture
def authenticated_client(api_client, create_user):
    """Authenticated API client"""
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def sample_geo_buckets(db):
    """Create sample geo buckets for testing"""
    buckets = []
    
    # Sangotedo area buckets
    sangotedo_bucket = GeoBucket.objects.create(
        name='Sangotedo',
        normalized_name='sangotedo',
        center=Point(3.6285, 6.4698),  # (lng, lat)
        radius_meters=1000,
        created_at=datetime.now() - timedelta(days=10)
    )
    buckets.append(sangotedo_bucket)
    
    # Sangotedo Phase 1 (close by, should be same bucket if within radius)
    sangotedo_phase1 = GeoBucket.objects.create(
        name='Sangotedo Phase 1',
        normalized_name='sangotedo phase 1',
        center=Point(3.6300, 6.4710),
        radius_meters=1000,
        created_at=datetime.now() - timedelta(days=5)
    )
    buckets.append(sangotedo_phase1)
    
    # Ikeja bucket (far away, different bucket)
    ikeja_bucket = GeoBucket.objects.create(
        name='Ikeja',
        normalized_name='ikeja',
        center=Point(3.3515, 6.6018),
        radius_meters=1000,
        created_at=datetime.now() - timedelta(days=15)
    )
    buckets.append(ikeja_bucket)
    
    # Empty bucket for testing
    empty_bucket = GeoBucket.objects.create(
        name='Empty Area',
        normalized_name='empty area',
        center=Point(3.5000, 6.5000),
        radius_meters=1000,
        created_at=datetime.now() - timedelta(days=20)
    )
    buckets.append(empty_bucket)
    
    return buckets


@pytest.fixture
def sample_properties(db, sample_geo_buckets):
    """Create sample properties for testing"""
    properties = []
    
    sangotedo_bucket = sample_geo_buckets[0]  # Sangotedo bucket
    ikeja_bucket = sample_geo_buckets[2]      # Ikeja bucket
    
    # Properties in Sangotedo
    prop1 = Property.objects.create(
        title='Luxury Villa Sangotedo',
        location_name='Sangotedo',
        location=Point(3.6285, 6.4698),
        price=75000000,
        bedrooms=5,
        bathrooms=4,
        geo_bucket=sangotedo_bucket,
        created_at=datetime.now() - timedelta(days=2)
    )
    properties.append(prop1)
    
    prop2 = Property.objects.create(
        title='Modern Duplex Sangotedo',
        location_name='Sangotedo',
        location=Point(3.6290, 6.4700),
        price=85000000,
        bedrooms=6,
        bathrooms=5,
        geo_bucket=sangotedo_bucket,
        created_at=datetime.now() - timedelta(days=1)
    )
    properties.append(prop2)
    
    prop3 = Property.objects.create(
        title='Affordable Bungalow Sangotedo',
        location_name='Sangotedo Estate',
        location=Point(3.6275, 6.4685),
        price=35000000,
        bedrooms=3,
        bathrooms=2,
        geo_bucket=sangotedo_bucket,
        created_at=datetime.now() - timedelta(hours=12)
    )
    properties.append(prop3)
    
    # Properties in Ikeja
    prop4 = Property.objects.create(
        title='Ikeja Office Space',
        location_name='Ikeja CBD',
        location=Point(3.3500, 6.6020),
        price=300000000,
        bedrooms=0,
        bathrooms=10,
        geo_bucket=ikeja_bucket,
        created_at=datetime.now() - timedelta(days=5)
    )
    properties.append(prop4)
    
    prop5 = Property.objects.create(
        title='Ikeja Family House',
        location_name='Ikeja GRA',
        location=Point(3.3495, 6.6015),
        price=68000000,
        bedrooms=4,
        bathrooms=3,
        geo_bucket=ikeja_bucket,
        created_at=datetime.now() - timedelta(days=3)
    )
    properties.append(prop5)
    
    return properties