from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from x007007007.djapp.localnet.nameserver.models import DomainModel
from x007007007.djapp.localnet.nameserver.models import RecordModel
from x007007007.djapp.localnet.zeroconf.models import DeviceModel
import string
import logging

LOGGER = logging.getLogger(__name__)


@receiver(signal=post_save, sender=DeviceModel)
def when_zero_conf_device_change(sender, instance: DeviceModel, **kwargs):
    inter_domain, _ = DomainModel.objects.get_or_create(name='device.internal')
    local_domain, _ = DomainModel.objects.get_or_create(name='local')
    host_name = ''.join((c for c in instance.name.lower() if c in (string.ascii_letters + string.digits + ".")))
    for ip in instance.ip_set.all():
        for domain in [inter_domain, local_domain]:
            RecordModel.objects.update_or_create(
                defaults=dict(
                    enable=True,
                    value=ip.ip,
                    type='A',
                    ttl=10*60,
                ),
                domain=domain,
                name=host_name
            )
