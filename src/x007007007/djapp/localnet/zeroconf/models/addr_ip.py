from x007007007.djapp import _models


class AddrIpModel(_models.Model):
    ip = _models.GenericIPAddressField()

    def __str__(self):
        return f"<IP {self.ip}>"
