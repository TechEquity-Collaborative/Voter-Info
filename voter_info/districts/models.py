
import django
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry


# a custom queryset and manager to be able to write:
# District.objects.contains_point(lat, lon) -> QuerySet[ <Area 1>, <Area 2>,... ]
class DistrictQuerySet(models.QuerySet):
    def contains_point(self, lat, lon):
        return self.filter(areas__mpoly__contains=GEOSGeometry(f'POINT({lon} {lat})')).distinct('id')


class DistrictManager(models.Manager):
    def get_queryset(self):
        return DistrictQuerySet(self.model, using=self._db)

    def contains_point(self, lat, lon):
        return self.get_queryset().contains_point(lat, lon)


class District(models.Model):
    """
    A district that's electing an office. Can have many areas,
    as specified by our 3rd-party shapefiles.
    """
    objects = DistrictManager()
    name = models.TextField()

    shape_file_name = models.TextField()

    def __repr__(self):
        return f'<District id={self.id} name={self.name}>'


# a custom queryset and manager to be able to write:
# Area.objects.contains_point(lat, lon) -> QuerySet[ <Area 1>, <Area 2>,... ]
class AreaQuerySet(models.QuerySet):
    def contains_point(self, lat, lon):
        return self.filter(mpoly__contains=GEOSGeometry(f'POINT({lon} {lat})'))


class AreaManager(models.Manager):
    def get_queryset(self):
        return AreaQuerySet(self.model, using=self._db)

    def contains_point(self, lat, lon):
        return self.get_queryset().contains_point(lat, lon)


class Area(models.Model):
    """
    A geographic area. The external shape files we are using
    have many areas within an office's district, e.g.
    a city-wide compaign can have multiple geographic areas for a
    given district (e.g. the whole city)
    """
    objects = AreaManager()

    district = models.ForeignKey(
        District,
        on_delete=django.db.models.deletion.CASCADE,
        related_name='areas',
        # not actually allowed to be true, but the GEODJango
        # libraries create Area instances before we can set the
        # foreign key
        null=True
    )

    name = models.CharField(max_length=50)

    # a json field corresponding to the attributes in the shapefile.
    # each shapefile can have a different schema.
    # you can find these fields with the `ogrinfo` shell utility
    # installed with the GIS libraries.
    # https://docs.djangoproject.com/en/2.0/ref/contrib/gis/tutorial/#use-ogrinfo-to-examine-spatial-data
    # or programatically with
    extra_fields = JSONField(encoder=DjangoJSONEncoder, null=True)

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    def __repr__(self):
        return f'<Area id={self.id} name={self.name} district={self.district}>'


# TODO(benmathes): if the district shapefiles have different schemas (e.g. model fields are custom
# to each shapefile), we can use ogrinspect to auto-generate models
# https://docs.djangoproject.com/en/2.0/ref/contrib/gis/tutorial/#try-ogrinspect
