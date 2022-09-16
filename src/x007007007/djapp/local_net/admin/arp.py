from django.contrib import admin

from ..models import ArpModel


@admin.register(ArpModel)
class ArpModelAdmin(admin.ModelAdmin):
    list_display = (
        'ip',
        'mac',
    )