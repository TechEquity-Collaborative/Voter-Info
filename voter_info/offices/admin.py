from django.contrib import admin

from offices.models import Office, Candidate


admin.site.register(Candidate)


class CandidateInline(admin.StackedInline):
    model = Candidate


class OfficeAdminWithCandidates(admin.ModelAdmin):
    inlines = [CandidateInline]


admin.site.register(Office, OfficeAdminWithCandidates)
