from django.contrib import admin

from ..models import AddrIpModel


@admin.register(AddrIpModel)
class AddrIpModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ip',
    )