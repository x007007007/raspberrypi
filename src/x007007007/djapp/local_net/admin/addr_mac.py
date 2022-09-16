from django.contrib import admin

from ..models import AddrMacModel


@admin.register(AddrMacModel)
class AddrMacModelAdmin(admin.ModelAdmin):
    list_display = (
        'mac',
    )