from x007007007.djapp import _models


class RecordQuerySet(_models.QuerySet):

    def available(self):
        return self.filter(enable=True)


class RecordModel(_models.Model):
    objects = RecordQuerySet.as_manager()
    domain = _models.ForeignKey("DomainModel", on_delete=_models.CASCADE)
    name = _models.CharField(max_length=254)
    value = _models.TextField()
    type = _models.CharField(max_length=8, choices=(
        ("A", "A"),
        ("AAAA", "AAAA"),
        ("CNAME", "CNAME"),
        ("MX", "MX"),
        ("NS", "NS"),
        ("TXT", "TXT"),
    ))
    ttl = _models.PositiveIntegerField(default=10*60)
    enable = _models.BooleanField(default=False)

