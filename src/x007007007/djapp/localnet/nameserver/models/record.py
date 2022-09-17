from x007007007.djapp import _models


class RecordModel(_models.Model):
    domain = _models.ForeignKey("DomainModel", on_delete=_models.CASCADE)
    value = _models.CharField(max_length=254)
    type = _models.CharField(max_length=8, choices=(
        ("A", "A"),
        ("AAAA", "AAAA"),
        ("CNAME", "CNAME"),
        ("MX", "MX"),
        ("NS", "NS"),
        ("TXT", "TXT"),
    ))
    enable = _models.BooleanField(default=False)

