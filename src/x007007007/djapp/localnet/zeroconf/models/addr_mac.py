from x007007007.djapp import _models


class AddrMacModel(_models.Model):
    mac = _models.CharField(max_length=12, default='', blank=True)

