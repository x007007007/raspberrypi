from x007007007.djapp import _models


class ServerModel(_models.Model):
    name = _models.CharField(max_length=254)
    device = _models.ForeignKey('DeviceModel', on_delete=_models.CASCADE)
    offline = _models.BooleanField(default=False)

