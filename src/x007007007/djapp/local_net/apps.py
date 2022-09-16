from django.apps import AppConfig
from .component.zeroconf import start

class X007DjAppLocalNetAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'x007007007.djapp.local_net'
    label = 'x7_local_net'
    url_prefix = 'api/'


    def ready(self):
        start()
