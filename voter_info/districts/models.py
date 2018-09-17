from django.db import models


class District(models.Model):
    """
    A district (jurisdictional area) that an office belongs to.
    E.g. "San Francisco", "County of Alameda", etc.

    Mostly just a grouping of offices.
    """
    name = models.TextField()

    def __repr__(self):
        return f'<District id={self.id} name="{self.name}">'

    def __str__(self):
        return self.__repr__()
