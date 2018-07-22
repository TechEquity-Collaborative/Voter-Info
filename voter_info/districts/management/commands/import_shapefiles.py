import os
import csv
import shutil
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile, BadZipFile
from pathlib import Path

from django.db import transaction
from django.core.management import BaseCommand
from django.contrib.gis.utils import LayerMapping

import districts
from districts.models import District, Area
from offices.models import Office

DISTRICTS_APP_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(districts.__file__)))

OFFICE_TO_SHAPEFILE_URLS_CSV_FILENAME = 'Bay Area Elected Offices - District Boundary File Links.csv'

DJANGO_MODEL_TO_SHAPEFILE_KEY = {
    'mpoly': 'MULTIPOLYGON',
}


class Command(BaseCommand):
    help = "idempotently imports all shapefiles linked to by voter_info/districts/{OFFICE_TO_SHAPEFILE_URLS_CSV_FILENAME}"

    @transaction.atomic
    def handle(self, *args, **options):
        self.download_shapefiles_from_urls_in_csv()
        self.extract_shapefiles_into_database()

    def download_shapefiles_from_urls_in_csv(self):
        """
        The TEC spreadsheet lists all offices and URL download links to appropriate shapefiles.
        This method reads the CSV (in OFFICE_TO_SHAPEFILE_URLS_CSV_FILENAME), and downloads
        the zipfiles at the linked URLs. The urls are then extracted into the districts/shape_files
        folder.

        After zipfile extraction, the shapefiles are loaded into the postgres database as Districts and Offices
        """
        csv_with_positions_and_districts = f'{DISTRICTS_APP_DIRECTORY}/{OFFICE_TO_SHAPEFILE_URLS_CSV_FILENAME}'

        with open(csv_with_positions_and_districts) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                district = row['Jurisdiction Level']
                office = row['Office']
                shapefile_archive_download_link = row['linkurl']
                print(f"Getting shapefiles for {district} - {office}")
                try:
                    response = urlopen(shapefile_archive_download_link)
                except Exception as e:
                    print(f"    error downloading from {shapefile_archive_download_link}: {e}")

                # make a directory in voter_info/districts/shape_files/$district/$offfice/
                try:
                    zipfile = ZipFile(BytesIO(response.read()))
                except BadZipFile as e:
                    print(f"    url does not have a zip of shapefiles: {shapefile_archive_download_link}")
                    continue
                # extract into a jurisidction/office tree folder structure.
                relative_path = f'shape_files/{district}/{office}/'
                target_extraction_path = f'{DISTRICTS_APP_DIRECTORY}/{relative_path}'
                # empty out any old shapefiles in there.
                try:
                    shutil.rmtree(target_extraction_path)
                    print(f"    cleaned old shapefiles in {relative_path}")
                except FileNotFoundError:
                    pass
                print(f"    extracting to {relative_path}")
                zipfile.extractall(target_extraction_path)

                return

    def extract_shapefiles_into_database(self):
        # iterate over every directory in districts/shape_files/$jurisidiction/$office/
        pathlist = Path(f'{DISTRICTS_APP_DIRECTORY}/shape_files/').glob('**/*.shp')
        self.already_connected_area_ids = set()
        for shape_file_path in pathlist:
            full_path = '/'.join(shape_file_path.parts)

            # different zip files contain different tree structures within /shape_files/$district/$office,
            # so we find the location in the path of "shape_files", and then take the next two indexes to
            # extrat the jurisidction and office
            root_shape_file_directory_index = shape_file_path.parts.index('shape_files')

            district_name = shape_file_path.parts[root_shape_file_directory_index + 1]
            office_name = shape_file_path.parts[root_shape_file_directory_index + 2]

            district, created = District.objects.get_or_create(name=district_name)
            if not created:
                print(f'district "{district_name}" already imported')
            else:
                self.create_areas_and_districts(district, full_path)

            self.create_offices_for_districts(district, office_name)

    def create_areas_and_districts(self, district, full_path):
        print(f'importing district: "{district.name}"')
        layer_mapping = LayerMapping(
            Area,
            full_path,
            DJANGO_MODEL_TO_SHAPEFILE_KEY,
            transform=False,
            encoding='iso-8859-1',
        )
        layer_mapping.save(strict=True)

        areas_to_save_to_district = Area.objects.exclude(id__in=self.already_connected_area_ids)
        for area in areas_to_save_to_district.all():
            area.district = district
            area.save()
            self.already_connected_area_ids.add(area.id)
        assert(Area.objects.filter(district_id__isnull=True).count() == 0)

    def create_offices_for_districts(self, district, office_name):
        office_for_district, was_created = Office.objects.get_or_create(name=office_name, district=district)
        print(f'created office: {office_for_district} for district: {district}')
