from django.apps import AppConfig
from logpipe import Consumer, register_consumer


class TicketingConfig(AppConfig):
    name = 'ticketing'


@register_consumer
def ticket_consumer():
    from .serializers import TicketSerializer

    consumer = Consumer('tickets')
    consumer.register(TicketSerializer)
    return consumer
