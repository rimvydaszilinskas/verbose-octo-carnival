from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

from rest_framework import serializers

from .constants import TicketClasses
from .models import Ticket, Sale
from .utils import send_to_acc


class ClassSerializer(serializers.Serializer):
    class_type = serializers.IntegerField(min_value=0, max_value=2)
    rows = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=50)
    )


class LiteTicketSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, format='hex')
    seat = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            'uuid',
            'seat',
            'flight',
            'flight_time'
        )

    def get_seat(self, obj):
        if isinstance(obj, Ticket):
            return '{}{}'.format(obj.row, chr(obj.column + 64))
        return None


class TicketSerializer(serializers.ModelSerializer):
    MESSAGE_TYPE = settings.TICKET_CREATION_MESSAGE_TYPE
    VERSION = 1

    rows = serializers.IntegerField(min_value=1, max_value=50, write_only=True)
    columns = serializers.IntegerField(
        min_value=1, max_value=12, write_only=True)
    flight = serializers.CharField(
        min_length=5, max_length=64)
    flight_time = serializers.DateTimeField(required=False)
    classes = ClassSerializer(write_only=True, required=False, many=True)

    uuid = serializers.UUIDField(read_only=True, format='hex')
    seat = serializers.SerializerMethodField()
    passenger_reference = serializers.CharField(
        read_only=True, source='passenger_ref')
    passenger_name = serializers.CharField(read_only=True)
    checked_in = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'uuid',
            'seat',
            'passenger_reference',
            'passenger_name',
            'checked_in',
            'rows',
            'columns',
            'flight',
            'flight_time',
            'classes',
        )

    def get_seat(self, obj):
        if isinstance(obj, Ticket):
            return '{}{}'.format(obj.row, chr(obj.column + 64))
        return None

    def validate_flight(self, flight):
        if self.instance is None and Ticket.objects.filter(flight=flight).exists():
            raise serializers.ValidationError('Flight already created')
        return flight

    def validate_classes(self, classes):
        for c in classes:
            if c['class_type'] not in TicketClasses.ALL:
                raise serializers.ValidationError(
                    '{} is not in ticket classes'.format(c['class_type']))

        return classes

    def create(self, validated_data):
        columns = validated_data['columns']
        rows = validated_data['rows']
        flight = validated_data['flight']
        flight_time = validated_data.get('flight_time', None)
        classes = validated_data.get('classes', [])
        tickets = []

        for column in range(columns):
            for row in range(rows):
                ticket = Ticket(
                    row=row+1,
                    column=column+1,
                    flight=flight)

                if flight_time:
                    ticket.flight_time = flight_time

                ticket.save()
                tickets.append(ticket)

        for c in classes:
            class_type = c['class_type']
            rows = c['rows']

            Ticket.objects.filter(flight=flight, row__in=rows).update(
                ticket_class=class_type)

        return tickets

    def save(self, *args, **kwargs):
        if self.instance is None:
            tickets = self.create(self.validated_data)

            return tickets

        return None


class SaleTicketSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(format='hex', required=True)
    passenger_reference = serializers.CharField(
        max_length=64, required=True, source='passenger_ref', write_only=True)
    passenger_name = serializers.CharField(max_length=64, required=True)
    checked_in = serializers.DateTimeField(read_only=True)
    seat = serializers.SerializerMethodField()

    def get_seat(self, obj):
        if isinstance(obj, Ticket):
            return '{}{}'.format(obj.row, chr(obj.column + 64))
        return None


class SaleSerializer(serializers.ModelSerializer):
    MESSAGE_TYPE = settings.NEW_SALE_MESSAGE_TYPE
    VERSION = 1

    uuid = serializers.UUIDField(format='hex', read_only=True)
    customer_reference = serializers.CharField(
        max_length=64, required=True, source='customer')
    customer_name = serializers.CharField(
        max_length=64, required=False)
    tickets = SaleTicketSerializer(many=True, required=True)
    paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Sale
        fields = (
            'uuid',
            'customer_reference',
            'customer_name',
            'tickets',
            'paid',
        )

    def validate_tickets(self, tickets):
        if len(tickets) == 0:
            raise serializers.ValidationError('No tickets')
        self.tickets = Ticket.objects.none()

        time = datetime.now() - timedelta(hours=1)

        for ticket in tickets:
            t = Ticket.objects.filter(uuid=ticket['uuid'])

            if not t.exists():
                raise serializers.ValidationError(
                    '{} ticket does not exist'.format(ticket['uuid']))
            elif self.tickets.filter(uuid=ticket['uuid']).exists():
                raise serializers.ValidationError(
                    '{} duplicate ticket'.format(ticket['uuid']))

            tt = t.first()

            if tt.sale:
                if tt.reserved and tt.reserved > time:
                    raise serializers.ValidationError(
                        '{} ticket is reserved'.format(ticket['uuid']))
                elif tt.sale.paid == True:
                    raise serializers.ValidationError(
                        '{} ticket is sold'.format(ticket['uuid']))

            self.tickets |= t

        return tickets

    def create(self, validated_data):
        sale = Sale.objects.create(
            customer=validated_data['customer'],
            customer_name=validated_data.get('customer_name', None)
        )

        self.tickets.update(reserved=datetime.now(), sale=sale)

        for t in validated_data['tickets']:
            ticket = self.tickets.get(uuid=t['uuid'])
            ticket.passenger_ref = t['passenger_ref']
            ticket.passenger_name = t['passenger_name']
            ticket.save()

        return sale

    def save(self, **kwargs):
        if self.instance is None:
            self.instance = self.create(self.validated_data)
            if not settings.TESTING:
                send_to_acc(self.instance)
        return self.instance

    @classmethod
    def lookup_instance(cls, uuid=None, **kwargs):
        try:
            return Sale.objects.get(uuid=uuid)
        except Sale.DoesNotExist:
            pass


class AccountingSaleSerializer(serializers.ModelSerializer):
    MESSAGE_TYPE = settings.ACCOUNTING_SALE_MESSAGE_TYPE
    VERSION = 1
    KEY_FIELD = 'uuid'

    uuid = serializers.UUIDField(format='hex', required=True)
    paid = serializers.BooleanField(required=True)
    customer = serializers.CharField(read_only=True)
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            'uuid',
            'paid',
            'customer',
            'tickets',
        )

    def get_tickets(self, obj):
        pas = obj.tickets.filter(ticket_class=TicketClasses.PASSENGER).count()
        bus = obj.tickets.filter(ticket_class=TicketClasses.BUSINESS).count()
        first = obj.tickets.filter(ticket_class=TicketClasses.FIRST).count()

        return {
            'passsenger': pas,
            'business': bus,
            'first': first
        }

    def validate(self, attrs):
        if self.instance:
            time = datetime.now() - timedelta(hours=1)

            if self.instance.created_at < time:
                raise serializers.ValidationError('Sale expired')

        return attrs

    def update(self, instance, validated_data):
        self.instance.paid = validated_data['paid']
        self.instance.save(update_fields=['paid'])
        return self.instance

    def save(self):
        if not self.instance:
            print('no instance')
            return

        self.instance = self.update(self.instance, self.validated_data)
        return self.instance

    @classmethod
    def lookup_instance(cls, uuid=None, **kwargs):
        try:
            return Sale.objects.get(uuid=uuid)
        except Sale.DoesNotExist:
            pass
