from rest_framework import serializers

from districts.models import District, Area
from offices.models import Office, Candidate


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


# we can't use offices.serializers, since that
# references the DistrictSerializer, which would be a circular import
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class OfficeWithoutDistricitsSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True)

    class Meta:
        model = Office
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    offices = OfficeWithoutDistricitsSerializer(many=True)

    class Meta:
        model = District
        fields = '__all__'
