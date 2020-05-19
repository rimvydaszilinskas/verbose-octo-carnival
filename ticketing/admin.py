from django.contrib import admin

from .models import Sale, Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'flight',
        'row',
        'column',
        'ticket_class',
        'uuid',
    )

    readonly_fields = (
        'uuid',
    )


class SaleAdmin(admin.ModelAdmin):
    readonly_fields = (
        'uuid',
    )


admin.site.register(Sale, SaleAdmin)
admin.site.register(Ticket, TicketAdmin)
