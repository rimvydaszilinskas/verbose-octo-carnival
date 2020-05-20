from datetime import datetime, timedelta

from rest_framework import views, status, generics
from rest_framework.response import Response

from django.db.models import Q

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


class SpecificTicketView(generics.ListAPIView):
    """
    List a specific ticket

    """
    serializer_class = TicketSerializer

    def get_queryset(self):
        sales = Sale.objects.all()

        purchased_tickets = self.request.GET.get('purchased_tickets', None)

        if purchased_tickets:
            sales = sales.filter(purchased_tickets=purchased_tickets)
        return sales


class CustomerPurchaseView(generics.ListAPIView):
    """
    List all customer purchase sales

    """
    serializer_class = SaleSerializer

    def get_queryset(self):
        sales = Sale.objects.filter(
            Q(reserved__isnull=True)
        ).filter(Q(sale=True) | Q(sale__paid=True))

        purchased_tickets = self.request.GET.get('purchased_tickets', None)

        if purchased_tickets:
            sales = sales.filter(purchased_tickets=purchased_tickets)
        return sales


