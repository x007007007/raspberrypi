from ... import _models


class DeviceTypeModel(_models.Model):
    name = _models.CharField(max_length=254)


