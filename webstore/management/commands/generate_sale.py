from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
import random

from webstore.models import Order

try:
    from faker import Faker
except Exception:
    Faker = None


class Command(BaseCommand):
    help = 'Generate fake sale transactions (Order model).'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=200000, help='Total number of orders to create')
        parser.add_argument('--batch', type=int, default=5000, help='Batch size for bulk_create')

    def handle(self, *args, **options):
        if Faker is None:
            self.stderr.write('Faker is required. Install with: pip install Faker')
            return

        count = options['count']
        batch_size = options['batch']
        fake = Faker()
        statuses = ['completed', 'pending', 'cancelled']

        start_index = Order.objects.count() + 1
        created = 0
        objs = []

        self.stdout.write(f'Starting generation: target={count}, batch={batch_size}')

        for i in range(count):
            idx = start_index + i
            order_number = f'ORDER{idx:012d}'
            customer_name = fake.name()
            status = random.choice(statuses)
            created_at = fake.date_time_between(start_date='-2y', end_date='now', tzinfo=timezone.get_current_timezone())

            objs.append(Order(order_number=order_number, customer_name=customer_name, status=status, created_at=created_at))

            if len(objs) >= batch_size:
                with transaction.atomic():
                    Order.objects.bulk_create(objs, batch_size=batch_size)
                created += len(objs)
                objs = []
                self.stdout.write(f'Created {created}/{count}')

        if objs:
            with transaction.atomic():
                Order.objects.bulk_create(objs, batch_size=batch_size)
            created += len(objs)
            self.stdout.write(f'Created {created}/{count}')

        self.stdout.write(self.style.SUCCESS(f'Done — created {created} orders'))
