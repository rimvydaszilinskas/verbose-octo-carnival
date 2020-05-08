import uuid

from django.db import models

from .constants import TicketClasses


class Ticket(models.Model):
    """
    Ticket model definition

    If passenger ref and sale is not set ticket is available
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    flight = models.CharField(max_length=64)
    reserved = models.DateTimeField(null=True, blank=True)
    ticket_class = models.PositiveSmallIntegerField(
        default=TicketClasses.PASSENGER,
        choices=TicketClasses.OPTIONS)
    flight_time = models.DateTimeField(null=True, blank=True)
    row = models.PositiveSmallIntegerField()
    column = models.PositiveSmallIntegerField()
    sale = models.ForeignKey(
        'ticketing.Sale', on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')

    passenger_ref = models.CharField(max_length=64, null=True, blank=True)
    passenger_name = models.CharField(max_length=255, null=True, blank=True)

    checked_in = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['flight', 'passenger_ref'])
        ]


class Sale(models.Model):
    """
    Sale holds tickets
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=64)
    customer_name = models.CharField(max_length=64, null=True, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['customer'])
        ]
