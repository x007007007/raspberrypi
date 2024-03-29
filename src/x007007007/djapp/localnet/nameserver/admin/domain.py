from django.contrib import admin

from ..models import DomainModel


@admin.register(DomainModel)
class DomainModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'enable',
    )

    list_filter = (
        'enable',
    )

    search_fields = (
        'name',
    )