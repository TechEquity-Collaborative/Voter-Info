import os
import csv
import shutil
import pathlib
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile, BadZipFile

from django.db import transaction
from django.core.management import BaseCommand
from django.contrib.gis.utils import LayerMapping

import districts
from districts.models import District, Area
from offices.models import Office


# it's fine if the public can see this URL -- all it provides is the ability the *view* the spreadsheet,
# but nobody can edit it. Worth noting that all the information in that sheet is about public officials,
# public offices, and other public information.
GOOGLE_SHEET_CSV_DOWNLOAD_URL = 'https://docs.google.com/spreadsheets/d/1oj1fc_CODd0waEYQFqluQhl8zZP0qjMNJHN0DlFfHr8/export?format=csv&id=1oj1fc_CODd0waEYQFqluQhl8zZP0qjMNJHN0DlFfHr8&gid=1344433296'

DISTRICTS_APP_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(districts.__file__)))

OFFICE_TO_SHAPEFILE_URLS_CSV_FILENAME = 'Bay Area Elected Offices - District Boundary File Links.csv'

CSV_WITH_POSITIONS_AND_DISTRICTS = f'{DISTRICTS_APP_DIRECTORY}/source_csv/{OFFICE_TO_SHAPEFILE_URLS_CSV_FILENAME}'

DJANGO_MODEL_TO_SHAPEFILE_KEY = {
    'mpoly': 'MULTIPOLYGON',
}


class Command(BaseCommand):
    help = "idempotently imports all shapefiles linked to by voter_info/districts/{OFFICE_TO_SHAPEFILE_URLS_CSV_FILENAME}"

    @transaction.atomic
    def handle(self, *args, **options):
        self.download_district_boundary_csv()
        self.download_shapefiles_from_urls_in_csv()

    def download_district_boundary_csv(self):
        response = urlopen(GOOGLE_SHEET_CSV_DOWNLOAD_URL)
        csv_contents = response.read()
        # 'wb' mode is the mode to write bytes to the file. the urlopen response.read() object returns
        # bytes, not a string. We just write the bytes directly to not futz with unicode conversion at all
        with open(CSV_WITH_POSITIONS_AND_DISTRICTS, 'wb') as csv_with_positions_and_districts:
            csv_with_positions_and_districts.write(csv_contents)

    def download_shapefiles_from_urls_in_csv(self):
        """
        The TEC spreadsheet lists all offices and URL download links to appropriate shapefiles.
        This method reads the CSV (in OFFICE_TO_SHAPEFILE_URLS_CSV_FILENAME), and downloads
        the zipfiles at the linked URLs. The urls are then extracted into the districts/shape_files
        folder.

        After zipfile extraction, the shapefiles are loaded into the postgres database as Districts and Offices
        """
        self.already_connected_area_ids = set()
        with open(CSV_WITH_POSITIONS_AND_DISTRICTS) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                district_name = row['Jurisdiction Level']
                office_name = row['Office']
                office_description = row['Office Description']
                shapefile_archive_download_link = row['linkurl']
                print(f"Importing shapefiles for {district_name} - {office_name}")
                try:
                    response = urlopen(shapefile_archive_download_link)
                except Exception as e:
                    print(f"    error downloading from {shapefile_archive_download_link}: {e}")

                # make a directory in voter_info/districts/shape_files/$district/$offfice/
                try:
                    zipfile = ZipFile(BytesIO(response.read()))
                except BadZipFile as e:
                    print(f"    *******************************************************************************")
                    print(f"    ERROR: error extracting file from shapefile link: {shapefile_archive_download_link}: {e}")
                    print(f"    *******************************************************************************")
                    continue
                # extract into a jurisidction/office tree folder structure.
                relative_path = f'shape_files/{district_name}/{office_name}/'
                target_extraction_path = f'{DISTRICTS_APP_DIRECTORY}/{relative_path}'
                # empty out any old shapefiles in there.
                try:
                    shutil.rmtree(target_extraction_path)
                    print(f"    cleaned old shapefiles in {relative_path}")
                except FileNotFoundError:
                    # it's ok if we tried to delete an old shapefile directory but there wasn't one
                    # there yet -- just means this is the first time we downloaded this shapefile
                    pass
                print(f"    extracting to {relative_path}")
                zipfile.extractall(target_extraction_path)
                self.extract_shapefile_into_database(target_extraction_path, district_name,
                                                     office_name, office_description)

    def extract_shapefile_into_database(self, extracted_folder_path, district_name, office_name, office_description):
        district, created = District.objects.get_or_create(name=district_name)
        if not created:
            print(f'    district "{district_name}" already imported')
        else:
            self.create_areas_and_district(district, extracted_folder_path)
        self.create_office_for_district(district, office_name, office_description)

    def create_areas_and_district(self, district, path_to_shapefile_zip_extraction):
        print(f'    importing district: "{district.name}"')
        # each zipfile can have different folder structure to the shapefile, so we
        # use pathlib to search down until it finds a '.shp' (shapefile)
        paths_to_shapefiles = pathlib.Path(path_to_shapefile_zip_extraction).glob('**/*.shp')
        paths = [path for path in paths_to_shapefiles]
        if len(paths) > 1:
            print(f"    More than one shapefile found for {path_to_shapefile_zip_extraction}")
        if len(paths) == 0:
            print(f"    *******************************************************************")
            print(f"    no shapefile found after extracting into {path_to_shapefile_zip_extraction}")
            print(f"    *******************************************************************")

        for path in paths:
            shapefile_path = '/'.join(path.parts)

            district.shape_file_name = shapefile_path
            district.save()

            # this instantiation and saving of the LayerMapping creats all the Area db rows
            # and saves them,
            layer_mapping = LayerMapping(Area, shapefile_path, DJANGO_MODEL_TO_SHAPEFILE_KEY,
                                         transform=False, encoding='iso-8859-1')
            layer_mapping.save(strict=True)

            areas_to_save_to_district = Area.objects.exclude(id__in=self.already_connected_area_ids)
            for area in areas_to_save_to_district.all():
                area.district = district
                area.save()
                self.already_connected_area_ids.add(area.id)
            assert(Area.objects.filter(district_id__isnull=True).count() == 0)

    def create_office_for_district(self, district, office_name, office_description):
        office_for_district, was_created = Office.objects.get_or_create(name=office_name, district=district)
        # the description can be modified in the TEC spreadsheet without us wanting to create
        # a new office db row.
        if office_for_district.description != office_description:
            office_for_district.description = office_description
            office_for_district.save()
        print(f'    {"created" if was_created else "updated"} office: {office_name} for district: {district.name}')
