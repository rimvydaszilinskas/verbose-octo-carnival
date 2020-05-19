from datetime import datetime, timedelta

from rest_framework import views, status, generics
from rest_framework.response import Response

from django.db.models import Q

from .models import Ticket
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
