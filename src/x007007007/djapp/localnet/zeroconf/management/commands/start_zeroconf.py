from django.core.management import BaseCommand
from x007007007.djapp.localnet.zeroconf.component.zeroconf import start

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         'node_name', help='node name for update',
    #     )

    def handle(self, *args, **options):
        start()



