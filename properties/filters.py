
import django_filters as filters
from django.db.models import QuerySet, F, Q
from django_filters import FilterSet
from django_filters.fields import DateRangeField as DjangoFilterDateRangeField
from django_filters.widgets import DateRangeWidget

from properties.models import Property


class DateRangeField(DjangoFilterDateRangeField):
    widget = DateRangeWidget


class DateRangeFilter(filters.DateFromToRangeFilter):
    field_class = DateRangeField



class PropertiesFilter(FilterSet):
    created_at = DateRangeFilter(field_name='created_at')
    search = filters.CharFilter(method="filter_search")

    @staticmethod
    def filter_search(queryset, _, value):
        return queryset.filter(
            Q(location_name__icontains=value)

        )

    class Meta:
        model = Property
        fields = ("created_at", )

