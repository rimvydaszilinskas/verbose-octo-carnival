from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tickets/$', views.TicketView.as_view()),
    url(r'^tickets/(?P<uuid>[0-9a-f]{32})/$',
        views.SpecificTicketView.as_view()),
    url(r'^customers/(?P<customer>\w+)/purchases/$',
        views.CustomerPurchaseView.as_view()),
    url(r'^sales/(?P<uuid>[0-9a-f]{32})/$', views.SaleView.as_view())
]
