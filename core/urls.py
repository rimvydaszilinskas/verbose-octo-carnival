from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'', include(('ticketing.urls', 'ticketing'), namespace='ticketing')),
    url(r'^admin/', admin.site.urls),
]
