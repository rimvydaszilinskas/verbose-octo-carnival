from datetime import datetime, timedelta

from rest_framework import views, status, generics
from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Ticket, Sale
from .serializers import TicketSerializer, SaleSerializer, LiteTicketSerializer


class TicketView(generics.ListAPIView):
    """
    List available tickets

    Add flight query param to filter by flight
    """
    serializer_class = LiteTicketSerializer

    def get_queryset(self):
        time = datetime.now() - timedelta(hours=1)

        tickets = Ticket.objects.filter(
            Q(reserved__isnull=True) | Q(reserved__lte=time)
        ).filter(Q(sale=None) | Q(sale__paid=False))

        flight = self.request.GET.get('flight', None)

        if flight:
            tickets = tickets.filter(flight=flight)
        return tickets


class SpecificTicketView(generics.RetrieveAPIView):
    """
    List a specific ticket
    """
    serializer_class = TicketSerializer

    def get_object(self):
        return get_object_or_404(Ticket, uuid=self.kwargs['uuid'], sale__paid=True)

    def post(self, request, *args, **kwargs):
        ticket = self.get_object()

        if ticket.checked_in is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Ticket already checked in'})

        ticket.checked_in = True
        ticket.save(update_fields=['checked_in'])

        return Response(self.serializer_class(ticket).data)


class CustomerPurchaseView(generics.ListAPIView):
    """
    List all customer purchase sales
    """
    serializer_class = SaleSerializer

    def get_queryset(self):
        sales = Sale.objects.filter(
            paid=True, customer=self.kwargs['customer'])

        return sales


class SaleView(generics.RetrieveAPIView):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    lookup_field = 'uuid'
