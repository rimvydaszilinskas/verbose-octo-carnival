from django.test import TestCase

from .models import Ticket
from .serializers import TicketSerializer


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
