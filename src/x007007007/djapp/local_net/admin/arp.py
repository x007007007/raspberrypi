from django.contrib import admin

from ..models import ArpModel


@admin.register(ArpModel)
class ArpAdminModel(admin.ModelAdmin):
    list_display = (
        'ip',
        'mac',
    )