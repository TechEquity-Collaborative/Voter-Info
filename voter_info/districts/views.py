from rest_framework.pagination import PageNumberPagination

from rest_framework import viewsets

from .serializers import DistrictSerializer
from .models import District


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    pagination_class = LargeResultsSetPagination
    http_method_names = ['get']
