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


@register_consumer
def new_sale_consumer():
    from .serializers import SaleSerializer

    consumer = Consumer('sales')
    consumer.register(SaleSerializer)
    return consumer


@register_consumer
def sale_consumer():
    from .serializers import AccountingSaleSerializer

    consumer = Consumer('acc_sales')
    consumer.register(AccountingSaleSerializer)
    return consumer
