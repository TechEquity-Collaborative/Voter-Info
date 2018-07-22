from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from offices.models import Office, Candidate
from offices.serializers import OfficeSerializer, CandidateSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    http_method_names = ['get']


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
