from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from zeroconf import ZeroconfServiceTypes
import socket
import ipaddress


class ZeroConfListener(ServiceListener):

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        from ..models import ServerModel, DeviceModel

        print("update_service")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        from ..models import ServerModel, DeviceModel
        ServerModel.objects.filter(
            name=name
        ).update(offline=True)
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        from ..models import ServerModel, DeviceModel, AddrIpModel
        info = zc.get_service_info(type_, name)

        device, _ = DeviceModel.objects.update_or_create(
            defaults=dict(
                offline=False
            ),
            name=info.get_name()
        )
        ip_list = []
        for ip in info.addresses:
            addr, _ = AddrIpModel.objects.get_or_create(ip=str(ipaddress.ip_address(ip)))
            ip_list.append(addr)
        old_ip_pk_list = set(device.ip_set.values_list('pk', flat=True))
        new_ip_pk_list = {i.pk for i in ip_list}

        for remove_pk in list(old_ip_pk_list - new_ip_pk_list):
            if remove_ip := AddrIpModel.objects.filter(pk=remove_pk).first():
                device.ip_set.remove(remove_ip)
        for new_create in (i for i in ip_list if i.pk in (new_ip_pk_list - old_ip_pk_list)):
            device.ip_set.add(new_create)

        server = ServerModel.objects.update_or_create(
            defaults=dict(
                offline=False
            ),
            name=info.name,
            device=device
        )
        print(f"Service {name} added, service info: {info.host_ttl}")


def start():
    zeroconf = Zeroconf(unicast=True)
    listener = ZeroConfListener()
    browser = ServiceBrowser(zeroconf, list(ZeroconfServiceTypes.find()), listener)
    browser.join()