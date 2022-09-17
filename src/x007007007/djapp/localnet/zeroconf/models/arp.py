from x007007007.djapp import _models


class ArpModel(_models.Model):
    ip = _models.ForeignKey("AddrIpModel", on_delete=_models.CASCADE)
    mac = _models.ForeignKey("AddrMacModel", on_delete=_models.CASCADE)
