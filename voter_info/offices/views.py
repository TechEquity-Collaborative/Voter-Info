from rest_framework import viewsets

from offices.models import Office, Candidate
from offices.serializers import OfficeSerializer, CandidateSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    http_method_names = ['get']


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    http_method_names = ['get']

