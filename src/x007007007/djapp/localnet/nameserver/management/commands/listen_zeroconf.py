from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'node_name', help='node name for update',
        )
        parser.add_argument(
            'src', help='local file or folder',
        )
        parser.add_argument(
            'dest', help='remote path',
        )

    def handle(self, *args, **options):
        pass


