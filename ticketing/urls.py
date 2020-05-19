from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tickets/$', views.TicketView.as_view()),
]
