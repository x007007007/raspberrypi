from django.contrib import admin

from ..models import DeviceTypeModel


@admin.register(DeviceTypeModel)
class DeviceTypeModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )