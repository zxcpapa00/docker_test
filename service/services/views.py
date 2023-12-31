from django.db.models import Prefetch, F, Sum

from django.shortcuts import render
from rest_framework import viewsets

from clients.models import Client
from services.models import Subscription
from .serializers import SubscriptionSerializers


class SubscriptionView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related(
            'user').only('company_name',
                         'user__email'))
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        response.data = response_data

        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')

        return response
