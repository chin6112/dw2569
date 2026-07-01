from django.core.management.base import BaseCommand

from clickhouse_connect.driver.exceptions import OperationalError

from webstore.clickhouse import sync_orders_to_clickhouse


class Command(BaseCommand):
    help = 'Sync orders from Django to ClickHouse.'

    def add_arguments(self, parser):
        parser.add_argument('--batch', type=int, default=5000, help='Batch size for ClickHouse insert')
        parser.add_argument('--limit', type=int, default=None, help='Optional max number of orders to sync')

    def handle(self, *args, **options):
        batch = options['batch']
        limit = options['limit']

        try:
            inserted = sync_orders_to_clickhouse(batch_size=batch, limit=limit)
        except OperationalError:
            self.stderr.write(
                'Could not connect to ClickHouse. Confirm the ClickHouse server is running at '
                'CLICKHOUSE_HOST:CLICKHOUSE_PORT and that the HTTP interface is enabled.'
            )
            return

        self.stdout.write(self.style.SUCCESS(f'Successfully inserted {inserted} orders into ClickHouse.'))
