from django.contrib import admin

from ..models import RecordModel


@admin.register(RecordModel)
class RecordModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'value',
        'type',
        'domain',
    )