from ... import _models


class ArpModel(_models.Model):
    ip = _models.GenericIPAddressField()
    mac = _models.CharField(max_length=12, default='', blank=True)
