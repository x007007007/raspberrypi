from django.core.management import BaseCommand
from x007007007.djapp.localnet.nameserver.component.server import main

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         'node_name', help='node name for update',
    #     )

    def handle(self, *args, **options):
        main()


