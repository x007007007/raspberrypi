from django.contrib import admin

from ..models import DeviceModel


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'offline',
    )

    readonly_fields = [
        'ip_set',
    ]