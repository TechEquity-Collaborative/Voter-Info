from django.contrib import admin
from django.db import transaction

from offices.models import Office, Area
from districts.models import District
from districts.management.commands.import_shapefiles import Command as IngestShapefilesCommand


@transaction.atomic
def ingest_shapefile_from_csv(model_admin, request, queryset):
    '''
    this function is run when you're in the District admin UI
    and run "ingest shapefiles from CSV"
    '''
    ingester = IngestShapefilesCommand()
    ingester.handle()


# docs here: docs.djangoproject.com/en/1.11/ref/contrib/admin/actions/#adding-actions-to-the-modeladmin
ingest_shapefile_from_csv.short_description = 'Ingest offices. Takes several minutes. Ok to run multiple times.'


class OfficeInline(admin.StackedInline):
    model = Office


class DistrictAdmin(admin.ModelAdmin):
    actions = admin.ModelAdmin.actions + [ingest_shapefile_from_csv]
    inlines = [OfficeInline]


admin.site.register(District, DistrictAdmin)
admin.site.register(Area)
