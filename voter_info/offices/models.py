from django.db import models

from districts.models import District


class Office(models.Model):
    class Meta:
        unique_together = (('name', 'district'),)

    name = models.TextField(null=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=False)


class Candidate(models.Model):
    class Meta:
        unique_together = (
            ('name', 'office'),
        )

    name = models.TextField(null=False)
    incumbent = models.BooleanField(default=False)
    url = models.TextField(null=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=False)
