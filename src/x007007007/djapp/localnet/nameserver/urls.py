from django.urls import path, include
from . import restapi

urlpatterns = [
    path('localnet/nameserver/domain/', restapi.domain.DomainListCreateAPIView.as_view()),
    path('localnet/nameserver/record/', restapi.record.RecordListCreateAPIView.as_view()),
]