from django.contrib import admin

from .models import Sale, Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'flight',
        'row',
        'column',
        'ticket_class',
    )


admin.site.register(Sale)
admin.site.register(Ticket, TicketAdmin)
