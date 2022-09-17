from ... import _models


class DeviceModel(_models.Model):
    name = _models.CharField(max_length=254)
    mac_set = _models.ManyToManyField(to="AddrMacModel", related_name="device_set")
    ip_set = _models.ManyToManyField(to="AddrIpModel", related_name="device_set")
    type = _models.ForeignKey("DeviceTypeModel", on_delete=_models.SET_NULL, null=True)
    offline = _models.BooleanField(default=False)

    def __str__(self):
        return f"<D: ({self.pk}) {self.name}>"
