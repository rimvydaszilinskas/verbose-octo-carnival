from rest_framework import views, status
from rest_framework.response import Response

from .serializers import TicketSerializer, SaleSerializer


class View(views.APIView):
    serializer_class = SaleSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        ser.save()

        return Response(ser.data)
