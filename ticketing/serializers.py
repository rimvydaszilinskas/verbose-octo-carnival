from rest_framework import serializers

from .constants import TicketClasses
from .models import Ticket, Sale


class ClassSerializer(serializers.Serializer):
    class_type = serializers.IntegerField(min_value=0, max_value=2)
    rows = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=50)
    )


class TicketSerializer(serializers.ModelSerializer):
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
            return '{}{}'.format(obj.row, chr(obj.seat + 64))
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
