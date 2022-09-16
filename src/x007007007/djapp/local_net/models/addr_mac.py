from ... import _models


class AddrMacModel(_models.Model):
    mac = _models.CharField(max_length=12, default='', blank=True)

