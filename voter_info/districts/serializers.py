from rest_framework import serializers

from districts.models import District, Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    # commented out b.c. there are MANY areas. slows server.
    # areas = AreaSerializer(many=True)

    class Meta:
        model = District
        fields = '__all__'
