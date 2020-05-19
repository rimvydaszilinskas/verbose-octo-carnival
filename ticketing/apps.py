from django.apps import AppConfig
from django.conf import settings

from logpipe import Consumer, register_consumer


class TicketingConfig(AppConfig):
    name = 'ticketing'


@register_consumer
def ticket_consumer():
    from .serializers import TicketSerializer

    consumer = Consumer(settings.TICKET_CREATION_TOPIC)
    consumer.register(TicketSerializer)
    return consumer


@register_consumer
def new_sale_consumer():
    from .serializers import SaleSerializer

    consumer = Consumer(settings.NEW_SALE_TOPIC)
    consumer.register(SaleSerializer)
    return consumer


@register_consumer
def sale_consumer():
    from .serializers import AccountingSaleSerializer

    consumer = Consumer(settings.ACCOUNTING_SALE_TOPIC)
    consumer.register(AccountingSaleSerializer)
    return consumer
