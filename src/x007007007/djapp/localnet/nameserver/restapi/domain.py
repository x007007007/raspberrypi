from rest_framework import generics
from rest_framework import serializers
from ..models import DomainModel


class DomainModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = DomainModel
        fields = [
            'name',
            'enable'
        ]


class DomainListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DomainModelSerializer
    queryset = DomainModel.objects.all()
    




