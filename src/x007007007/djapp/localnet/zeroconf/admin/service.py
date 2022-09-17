from django.contrib import admin

from ..models import ServerModel


@admin.register(ServerModel)
class ServerModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'device',
        'offline',
    )