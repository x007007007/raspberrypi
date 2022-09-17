from x007007007.djapp import _models


class DomainModel(_models.Model):
    name = _models.CharField(max_length=254)
    enable = _models.BooleanField(default=False)

