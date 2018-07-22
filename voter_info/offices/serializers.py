from rest_framework import serializers

from offices.models import Office, Candidate
from districts.serializers import DistrictSerializer


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class OfficeSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True)
    district = DistrictSerializer()

    class Meta:
        model = Office
        fields = '__all__'
