from django.contrib.gis.db import models as gis_models
from django.db import models

class GeoBucket(models.Model):
    """
    Logical geo-area bucket
    """
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255, db_index=True)

    center = gis_models.PointField(geography=True)
    radius_meters = models.IntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            gis_models.Index(fields=["center"]),
            models.Index(fields=["normalized_name"]),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.name
