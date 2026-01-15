from django.contrib.gis.db import models as gis_models
from django.db import models
from geo.models import GeoBucket

class Property(models.Model):
    title = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)

    location = gis_models.PointField(geography=True)

    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)

    geo_bucket = models.ForeignKey(
        GeoBucket,
        on_delete=models.PROTECT,
        related_name="properties"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            gis_models.Index(fields=["location"]),
            models.Index(fields=["geo_bucket"]),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.title

