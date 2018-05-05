import os

from django.core.management import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

import districts
from districts.models import District

WORLD_APP_DATA_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(districts.__file__)))

SHAPE_FILE_NAME = 'geo_export_efa8ecd8-3d0c-424b-bf93-d52b75f0e330.shp'

django_model_to_shapefile_key = {
    'fips' : 'FIPS',
    'iso2' : 'ISO2',
    'iso3' : 'ISO3',
    'un' : 'UN',
    'name' : 'NAME',
    'area' : 'AREA',
    'pop2005' : 'POP2005',
    'region' : 'REGION',
    'subregion' : 'SUBREGION',
    'lon' : 'LON',
    'lat' : 'LAT',
    'mpoly' : 'MULTIPOLYGON',
}


class Command(BaseCommand):
    help = "imports all shapefiles in world/data/"

    def handle(self, *args, **options):
        shape_file_path = f'{WORLD_APP_DATA_DIRECTORY}/shape_files/{SHAPE_FILE_NAME}'
        data_source = DataSource(shape_file_path)
        layer_mapping = LayerMapping(
            District,
            shape_file_path,
            django_model_to_shapefile_key,
            transform=False,
            encoding='iso-8859-1',
        )
        layer_mapping.save(strict=True, verbose=True)
