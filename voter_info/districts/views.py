from datetime import datetime, timedelta

from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination

from .serializers import DistrictSerializer, OfficeWithoutDistricitsSerializer, CandidateSerializer


from districts.models import District


class LatLongMissingException(APIException):
    # "Unprocessible Entity"
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422
    status_code = 422
    default_detail = '"lat" and "lon" are both required HTTP query params'
    default_code = 'lat_lon_required'


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    pagination_class = LargeResultsSetPagination
    http_method_names = ['get']

    def get_queryset(self):
        """
        This is how we make the Django Request Framework (DRF) run custom queries.
        By default get_queryset should return the django model queryset for all instances
        of the related class (district.models.Distric).

        If the caller is expecting a list, we allow for lat/long HTTP query params.
        Read more here:
        http://www.django-rest-framework.org/api-guide/filtering/#overriding-the-initial-queryset
        """
        if self.action == 'list':
            return self._lat_long_district_list_queryset()
        else:
            return District.objects.all()

    def _lat_long_district_list_queryset(self):
        # prefetch_related is how you get django to preload datat you know you'll
        # need in as few queries as possible. Turns # of queries from O(number of rows)
        # into O(number of relations).
        # https://docs.djangoproject.com/en/2.1/ref/models/querysets/#prefetch-related
        queryset = District.objects.all().prefetch_related('offices__candidates')

        lat = self.request.GET.get('lat')
        lon = self.request.GET.get('lon')

        if lat and lon:
            queryset = queryset.contains_point(lat, lon)

        return queryset
