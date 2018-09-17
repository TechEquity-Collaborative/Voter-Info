from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from offices.models import Office, Candidate
from offices.serializers import OfficeSerializer, CandidateSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    http_method_names = ['get']


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    http_method_names = ['get']

    def get_queryset(self):
        """
        This is how we make the Django Request Framework (DRF) run custom queries.
        By default get_queryset should return the django model queryset for all instances
        of the related class (offices.models.Distric).

        If the caller is expecting a list, we allow for lat/long HTTP query params.
        Read more here:
        http://www.django-rest-framework.org/api-guide/filtering/#overriding-the-initial-queryset
        """
        if self.action == 'list':
            return self._lat_long_district_list_queryset()
        else:
            return Office.objects.all()

    def _lat_long_district_list_queryset(self):
        # prefetch_related is how you get django to preload datat you know you'll
        # need in as few queries as possible. Turns # of queries from O(number of rows)
        # into O(number of relations).
        # https://docs.djangoproject.com/en/2.1/ref/models/querysets/#prefetch-related
        queryset = Office.objects.all().prefetch_related('candidates')\
                                       .prefetch_related('district')

        lat = self.request.GET.get('lat')
        lon = self.request.GET.get('lon')

        if lat and lon:
            queryset = queryset.contains_point(lat, lon)

        return queryset
