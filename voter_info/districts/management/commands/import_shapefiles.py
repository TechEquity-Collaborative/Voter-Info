import os
from pathlib import Path

from django.core.management import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

import districts
from districts.models import District

DISTRICTS_APP_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(districts.__file__)))

SHAPE_FILE_NAME = 'geo_export_d7286284-cf00-4f7f-bb87-739e415712fe.shp'# 'geo_export_efa8ecd8-3d0c-424b-bf93-d52b75f0e330.shp'

django_model_to_shapefile_key = {
    'mpoly' : 'MULTIPOLYGON',
}


# 1: one shapefile package per district (1-1 to office).
# 2: one shapefile may have many areas, which belong to one District. (so districts.models will have 2 models)
# 3: sub-directory each shapefile package.
# 4: try to ignore the "schema" of the shapefiles. just a name will do.

class Command(BaseCommand):
    help = "idempotently imports all shapefiles in voter_info/districts/shapefiles/"

    def handle(self, *args, **options):
        shape_file_path = {SHAPE_FILE_NAME}


        pathlist = Path(f'{DISTRICTS_APP_DIRECTORY}/shape_files/').glob('**/*.shp')
        import pdb; pdb.set_trace()
        for shape_file_path in pathlist:
            data_source = DataSource('/'.join(shape_file_path.parts))

            # TODO(benmathes): this layer mapping is failing. The django_model_to_shapefile_key
            # is from the geoDjango tutorial, which comes with its own shapefile. Perhaps the
            # mapping is peculiar to each shapefile?
            # https://docs.djangoproject.com/en/2.0/ref/contrib/gis/layermapping/
            layer_mapping = LayerMapping(
                Area,
                shape_file_path,
                django_model_to_shapefile_key,
                transform=False,
                encoding='iso-8859-1',
            )
            layer_mapping.save(strict=True, verbose=True)
