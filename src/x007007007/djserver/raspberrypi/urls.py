from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.apps import apps
import importlib


urlpatterns = [
    path('admin/', admin.site.urls),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

for app_config in apps.get_app_configs():
    app_package_name = ".".join(app_config.__class__.__module__.split(".")[:-1])
    url_module_name = f'{app_package_name}.urls'
    try:
        a = importlib.import_module(url_module_name)
        if a.__name__.startswith("x007007007"):
            if url_prefix := getattr(app_config, 'url_prefix'):
                urlpatterns.append(path(url_prefix, include(url_module_name)))
    except ImportError:
        pass

