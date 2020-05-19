from logpipe import Producer


def send_to_acc(instance):
    from .serializers import AccountingSaleSerializer

    producer = Producer('acc_sales', AccountingSaleSerializer)
    producer.send(instance)
