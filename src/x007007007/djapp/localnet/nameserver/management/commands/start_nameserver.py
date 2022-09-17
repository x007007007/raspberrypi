from django.core.management import BaseCommand
from x007007007.djapp.localnet.nameserver.component.server import main


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'port',
            help='port of dns server',
            type=int,
            default=53
        )

    def handle(self, *args, **options):
        main(options['port'])


