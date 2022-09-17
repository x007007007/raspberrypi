from x007007007.djapp import _models


class DomainQuerySet(_models.QuerySet):

    def available(self):
        return self.filter(enable=True)


class DomainModel(_models.Model):
    objects = DomainQuerySet.as_manager()

    name = _models.CharField(max_length=254)
    enable = _models.BooleanField(default=False)

    def __str__(self):
        return f'<Domain: ({self.pk}) .{self.name}>'