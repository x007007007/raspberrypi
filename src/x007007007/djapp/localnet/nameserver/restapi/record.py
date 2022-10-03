from rest_framework import generics
from rest_framework import serializers
from ..models import RecordModel
from .domain import DomainModelSerializer


class RecordModelSerializer(serializers.ModelSerializer):
    domain = DomainModelSerializer()

    class Meta:
        model = RecordModel
        fields = [
            'domain',
            'name',
            'value',
            'type',
            'ttl',
            'enable',
        ]


class RecordListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RecordModelSerializer
    queryset = RecordModel.objects.prefetch_related('domain').all()






