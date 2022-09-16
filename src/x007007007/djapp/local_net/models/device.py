from ... import _models


class DeviceModel(_models.Model):
    name = _models.CharField(max_length=254)
    mac = _models.CharField(max_length=12, default='', blank=True)
    type = _models.ForeignKey("DeviceTypeModel", on_delete=_models.SET_NULL, null=True)
