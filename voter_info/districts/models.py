from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry


# a custom queryset and manager to be able to write:
# District.objects.contains_point(lat, lon) -> QuerySet[ <District 1>, <District 2>,... ]
class DistrictQuerySet(models.QuerySet):
    def contains_point(self, lat, lon):
        return self.filter(mpoly__contains=GEOSGeometry(f'POINT({lat} {lon})'))


class DistrictManager(models.Manager):
    def get_queryset(self):
        return DistrictQuerySet(self.model, using=self._db)

    def contains_point(self, lat, lon):
        return self.get_queryset().contains_point(lat, lon)


class District(models.Model):

    objects = DistrictManager()

    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)

    # you can find these fields with the `ogrinfo` shell utility
    # installed with the GIS libraries.
    # https://docs.djangoproject.com/en/2.0/ref/contrib/gis/tutorial/#use-ogrinfo-to-examine-spatial-data
    shape_stle = models.FloatField('shape style')
    dist_name = models.TextField('district name')
    shape_star = models.FloatField('shape star')
    district_i = models.FloatField('district ID')

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name





# TODO(benmathes): if the district shapefiles have different schemas (e.g. model fields are custom
# to each shapefile), we can use ogrinspect to auto-generate models
# https://docs.djangoproject.com/en/2.0/ref/contrib/gis/tutorial/#try-ogrinspect
