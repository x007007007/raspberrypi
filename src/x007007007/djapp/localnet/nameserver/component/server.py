from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server
from x007007007.djapp.localnet.nameserver.models import DomainModel
from django.db.models.functions import Length
from x007007007.djapp.localnet.nameserver.models import RecordModel
import logging

LOGGER = logging.getLogger(__name__)


class DynamicResolver(object):

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

    def _doDynamicResponse(self, query):
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
                    print(record)
                    record = RecordModel.objects.available().filter(
                        domain=query.domain,
                        name='*',
                        type='A'
                    ).values('value', 'ttl')
                print(record)
                answers = [
                    dns.RRHeader(
                        name=name,
                        payload=dns.Record_A(
                            address=v['value'],
                            ttl=v['ttl'],
                        ))
                    for v in record
                ]
                print(answers)
                return answers, [], []
        return [], [], []

    def query(self, query, timeout=None):
        """
        Check if the query should be answered dynamically, otherwise dispatch to
        the fallback resolver.
        """
        if self._dynamicResponseRequired(query):
            return defer.succeed(self._doDynamicResponse(query))
        else:
            return defer.fail(error.DomainError())



def main():
    """
    Run the server.
    """
    factory = server.DNSServerFactory(
        clients=[DynamicResolver(), client.Resolver(resolv='/etc/resolv.conf')]
    )

    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(53, protocol)
    reactor.listenTCP(53, factory)

    reactor.run()


