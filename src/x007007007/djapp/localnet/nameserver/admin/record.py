from django.contrib import admin

from ..models import RecordModel


@admin.register(RecordModel)
class RecordModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'value',
        'type',
        'domain',
        'ttl',
        'enable'
    )

    list_filter = [
        'enable',
    ]