
import django_filters as filters
from django.db.models import QuerySet, F, Q
from django_filters import FilterSet
from django_filters.fields import DateRangeField as DjangoFilterDateRangeField
from django_filters.widgets import DateRangeWidget

from geo.models import GeoBucket
from properties.models import Property


class DateRangeField(DjangoFilterDateRangeField):
    widget = DateRangeWidget


class DateRangeFilter(filters.DateFromToRangeFilter):
    field_class = DateRangeField



class PropertiesFilter(FilterSet):
    created_at = DateRangeFilter(field_name='created_at')
    search = filters.CharFilter(method="filter_search")



    @staticmethod
    def filter_search(queryset,_, value):
        """Optimized location search using geo-buckets AND text search"""
        if not value:
            return queryset

        value = value.lower().strip()

        # 1. FIRST: Find matching buckets (Efficient - uses database)

        matching_buckets = GeoBucket.objects.filter(
            Q(normalized_name__icontains=value) |
            Q(name__icontains=value)
        ).values_list('id', flat=True)[:50]  # Limit results

        if matching_buckets:
            # 2. Use bucket IDs for efficient property lookup
            return queryset.filter(geo_bucket_id__in=list(matching_buckets))
        else:
            # 3. Fallback: Direct property search
            return queryset.filter(
                Q(location_name__icontains=value) |
                Q(geo_bucket__normalized_name__icontains=value)
            )


    class Meta:
        model = Property
        fields = ("created_at", )

