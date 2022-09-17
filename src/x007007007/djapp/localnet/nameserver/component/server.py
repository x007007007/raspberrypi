from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server
from x007007007.djapp.localnet.nameserver.models import DomainModel
from django.db.models.functions import Length
from x007007007.djapp.localnet.nameserver.models import RecordModel
import logging
import netifaces


LOGGER = logging.getLogger(__name__)


class DynamicResolver(object):
    """
    如果要实现 根据访问来源解析不同的dns记录，需要写DNSServerFactory 中的 resolver
    可以先实现
    """
    def __init__(self, interface):
        self.interface = interface

    def _dynamicResponseRequired(self, query: dns.Query):
        """
        Check the query to determine if a dynamic response is required.
        """
        match query.type:
            case dns.A:
                res = []
                current_domain_list = []
                for i in query.name.name.decode('utf8').split('.')[::-1]:
                    current_domain_list.append(i)
                    domain = ".".join(current_domain_list)
                    res.append(domain)
                if domain := DomainModel.objects.filter(
                        name__in=res
                ).order_by(Length('name').asc()).first():
                    query.domain = domain
                    return True
        return False

    def _doDynamicResponse(self, query: dns.Query):
        """
        Calculate the response to a query.
        :return: answers, authority:[], additional, []
        """
        match query.type:
            case dns.A:
                name = query.name.name.decode('utf-8')
                LOGGER.debug(f"user A query: {name}")
                label = name.removesuffix(f".{query.domain.name}")
                if len(record := RecordModel.objects.available().filter(
                    domain=query.domain,
                    name=label,
                    type='A',
                ).values('value', 'ttl')) == 0:
                    record = RecordModel.objects.available().filter(
                        domain=query.domain,
                        name='*',
                        type='A'
                    ).values('value', 'ttl')
                answers = [
                    dns.RRHeader(
                        name=name,
                        payload=dns.Record_A(
                            address=v['value'],
                            ttl=v['ttl'],
                        ))
                    for v in record
                ]
                return answers, [], []
        return defer.fail(error.DomainError())

    def query(self, query, timeout=None):
        """
        Check if the query should be answered dynamically, otherwise dispatch to
        the fallback resolver.
        """
        if self._dynamicResponseRequired(query):
            return defer.succeed(self._doDynamicResponse(query))
        else:
            return defer.fail(error.DomainError())


class PrintClientAddressDNSServerFactory(server.DNSServerFactory):

    def handleQuery(self, message, protocol, address):
        query = message.queries[0]
        return (
            self.resolver.query(query)
            .addCallback(self.gotResolverResponse, protocol, message, address)
            .addErrback(self.gotResolverError, protocol, message, address)
        )


class PrintClientAddressDNSDatagramProtocol(dns.DNSDatagramProtocol):
    def datagramReceived(self, datagram, addr):
        print("Datagram to DNSDatagramProtocol from {}".format(addr))
        return dns.DNSDatagramProtocol.datagramReceived(self, datagram, addr)


def iter_interface():
    for interface in netifaces.interfaces():
        for addr in netifaces.ifaddresses(interface).get(netifaces.AF_INET, []):
            yield addr

def main():
    """
    Run the server.
    """

    for addr in iter_interface():
        factory = PrintClientAddressDNSServerFactory(
            clients=[DynamicResolver(interface=addr), client.Resolver(resolv='/etc/resolv.conf')]
        )
        protocol = PrintClientAddressDNSDatagramProtocol(controller=factory)
        try:
            reactor.listenUDP(53, protocol, interface=addr['addr'])
        except:
            logging.exception('udp listen failed')
        try:
            reactor.listenTCP(53, factory, interface=addr['addr'])
        except:
            logging.exception('tcp listen failed')
    reactor.run()


