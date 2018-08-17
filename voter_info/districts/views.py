from rest_framework import viewsets

from districts.models import District
from districts.serializers import DistrictSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    http_method_names = ['get']
