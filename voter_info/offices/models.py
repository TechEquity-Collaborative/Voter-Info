from django.db import models

from districts.models import District


class Office(models.Model):
    class Meta:
        unique_together = (('name', 'district'),)

    name = models.TextField(null=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=False, related_name='offices')

    def __str__(self):
        return f'<Office id={self.id} name="{self.name}" district="{self.district.name}" district_id={self.district.id}>'



class Candidate(models.Model):
    class Meta:
        unique_together = (
            ('name', 'office'),
        )

    name = models.TextField(null=False)
    incumbent = models.BooleanField(default=False)
    url = models.TextField(null=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=False, related_name='candidates')

    def __str__(self):
        return f'<Candidate id={self.id} name="{self.name}" incumbent={self.incumbent} office="{self.office.name}" office_id={self.office.id} office_district="{self.office.district.name}">'
