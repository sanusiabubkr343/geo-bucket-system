from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeoBucketViewSet

router = DefaultRouter()
router.register(r'geo-buckets', GeoBucketViewSet, basename='geo-bucket')

urlpatterns = [
    path('', include(router.urls)),
]