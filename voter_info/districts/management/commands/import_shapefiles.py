import os
from pathlib import Path

from django.db import transaction
from django.core.management import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

import districts
from districts.models import District, Area

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
    help = "idempotently imports all shapefiles like voter_info/districts/shape_files/$districtName/shapefile.shp"

    @transaction.atomic
    def handle(self, *args, **options):
        shape_file_path = {SHAPE_FILE_NAME}

        pathlist = Path(f'{DISTRICTS_APP_DIRECTORY}/shape_files/').glob('**/*.shp')
        already_connected_area_ids = set()
        for shape_file_path in pathlist:
            full_path = '/'.join(shape_file_path.parts)
            data_source = DataSource(full_path)
            # path is .../districts/shape_files/$districtName/_some_geo_export_file.shp
            district_name = shape_file_path.parts[-2]
            district, created = District.objects.get_or_create(name=district_name)
            if not created:
                print(f'"{district_name}" already imported')
                continue
            else:
                print(f'importing "{district_name}"')

            layer_mapping = LayerMapping(
                Area,
                full_path,
                django_model_to_shapefile_key,
                transform=False,
                encoding='iso-8859-1',
            )
            layer_mapping.save(strict=True)

            # TODO(benmathes): figure out a way to get the Area instances created from the layer_mapping
            # currently not supported: http://grokbase.com/t/gg/django-updates/125qmmyy7j/django-18368-layermapping-save-should-be-able-to-set-attributes-on-created-model-instances
            areas_to_save_to_district = Area.objects.exclude(id__in=already_connected_area_ids)
            for area in areas_to_save_to_district.all():
                area.district = district
                area.save()
                already_connected_area_ids.add(area.id)
            assert(Area.objects.filter(district_id__isnull=True).count() == 0)
