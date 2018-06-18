from django.contrib import admin
from django.db import transaction

from districts.models import District, Area
from districts.management.commands.import_shapefiles import Command as IngestShapefilesCommand


@transaction.atomic
def ingest_shapefile_from_csv(model_admin, request, queryset):
    '''
    this function is run when you're in the District admin UI
    and run "ingest shapefiles from CSV"
    '''
    IngestShapefilesCommand.download_shapefiles_from_urls_in_csv()
    IngestShapefilesCommand.extract_shapefiles_into_database()


# docs here: docs.djangoproject.com/en/1.11/ref/contrib/admin/actions/#adding-actions-to-the-modeladmin
ingest_shapefile_from_csv.short_description = 'upserts the offices and districts from the CSV with district/office names and links to the shapefiles'


class DistrictAdmin(admin.ModelAdmin):
    actions = admin.ModelAdmin.actions + [ingest_shapefile_from_csv]


admin.site.register(District, DistrictAdmin)
admin.site.register(Area)
