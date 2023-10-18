from django.db.models import Prefetch

from django.shortcuts import render
from rest_framework import viewsets

from clients.models import Client
from services.models import Subscription
from .serializers import SubscriptionSerializers


class SubscriptionView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all().prefetch_related(
        Prefetch('client', queryset=Client.objects.all().select_related(
            'user').only('company_name',
                         'user__email'))
    )
