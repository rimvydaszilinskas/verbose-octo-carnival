from django.test import TestCase

from .models import Ticket, Sale
from .serializers import TicketSerializer, SaleSerializer


class TestTicketSerializer(TestCase):
    def test_create_40_tickets(self):
        data = {
            'rows': 10,
            'columns': 4,
            'flight': 'First flight ever',
            'classes': [
                {
                    'class_type': 1,
                    'rows': [
                        1, 2
                    ]
                },
                {
                    'class_type': 2,
                    'rows': [
                        3, 4
                    ]
                }
            ]
        }

        serializer = TicketSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        tickets = serializer.save()

        self.assertIsNotNone(tickets)
        self.assertEqual(Ticket.objects.all().count(), 40)
        self.assertEqual(Ticket.objects.filter(ticket_class=1).count(), 8)


class TestSaleSerializer(TestCase):
    def setUp(self):
        self.ticket1 = Ticket.objects.create(row=1, column=1, flight='abc')
        self.ticket2 = Ticket.objects.create(row=1, column=2, flight='abc')
        self.ticket3 = Ticket.objects.create(row=1, column=3, flight='abc')
        self.ticket4 = Ticket.objects.create(row=1, column=4, flight='abc')
        self.ticket5 = Ticket.objects.create(row=1, column=5, flight='abc')
        self.ticket6 = Ticket.objects.create(row=1, column=6, flight='abc')

    def test_create_sale(self):
        data = {
            'customer_reference': 'abcd',
            'tickets': [
                {
                    'uuid': self.ticket1.uuid.hex,
                    'passenger_name': 'name',
                    'passenger_reference': '777777'
                },
                {
                    'uuid': self.ticket2.uuid.hex,
                    'passenger_name': 'name1',
                    'passenger_reference': '666'
                }
            ]
        }

        serializer = SaleSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        sale = serializer.save()

        self.assertEqual(Sale.objects.all().count(), 1)
