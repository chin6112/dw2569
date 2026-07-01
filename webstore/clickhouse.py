import logging
import os
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

try:
    from clickhouse_connect import get_client
    from clickhouse_connect.driver.exceptions import ClickHouseError, OperationalError
except ImportError:  # pragma: no cover
    get_client = None
    ClickHouseError = Exception
    OperationalError = Exception

TABLE_NAME = 'orders'


def get_clickhouse_client():
    if get_client is None:
        raise ImportError('clickhouse-connect is not installed. Install with: pip install clickhouse-connect')

    config = settings.CLICKHOUSE
    try:
        return get_client(
            host=config['host'],
            port=config['port'],
            username=config['username'],
            password=config['password'],
            database=config['database'],
            secure=config['secure'],
        )
    except OperationalError as exc:
        logger.error(
            'Could not connect to ClickHouse at %s:%s. Is the ClickHouse server running and reachable?',
            config['host'], config['port'],
        )
        raise


def ensure_orders_table(client=None):
    if client is None:
        client = get_clickhouse_client()

    create_sql = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id Int64,
        order_number String,
        customer_name String,
        created_at DateTime,
        status String
    ) ENGINE = MergeTree()
    ORDER BY (id)
    '''.strip()

    logger.info('Creating ClickHouse table if missing: %s', TABLE_NAME)
    client.command(create_sql)


def _normalize_datetime(value):
    if value is None:
        return None
    if timezone.is_aware(value):
        return value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


def order_to_clickhouse_row(order):
    return {
        'id': order.id,
        'order_number': order.order_number,
        'customer_name': order.customer_name,
        'created_at': _normalize_datetime(order.created_at),
        'status': order.status,
    }


def sync_orders_to_clickhouse(batch_size=5000, limit=None, client=None):
    from .models import Order

    if client is None:
        client = get_clickhouse_client()

    ensure_orders_table(client)

    queryset = Order.objects.all().order_by('id')
    if limit is not None:
        queryset = queryset[:limit]

    total = queryset.count()
    inserted = 0

    for start in range(0, total, batch_size):
        batch = list(queryset[start:start + batch_size])
        if not batch:
            break

        rows = [order_to_clickhouse_row(order) for order in batch]
        try:
            client.insert(TABLE_NAME, rows, column_names=['id', 'order_number', 'customer_name', 'created_at', 'status'])
            inserted += len(rows)
            logger.info('Inserted batch %s - %s rows', start + 1, start + len(rows))
        except ClickHouseError as exc:
            logger.exception('ClickHouse insert failed for batch starting at %s', start)
            raise

    return inserted


def get_foursquare_catalog():
    from pyiceberg.catalog import load_catalog

    token = os.environ.get('FOURSQUARE_ACCESS_TOKEN')
    if not token:
        raise RuntimeError('Set FOURSQUARE_ACCESS_TOKEN in your environment first.')

    return load_catalog(
        'default',
        **{
            'warehouse': 'places',
            'uri': 'https://catalog.h3-hub.foursquare.com/iceberg',
            'token': token,
            'header.content-type': 'application/vnd.api+json',
            'rest-metrics-reporting-enabled': 'false',
        },
    )


def list_foursquare_namespaces():
    catalog = get_foursquare_catalog()
    return catalog.list_namespaces()


def list_foursquare_tables(namespace):
    catalog = get_foursquare_catalog()
    return catalog.list_tables(namespace)


def load_foursquare_places(limit=100):
    try:
        import polars as pl
    except ImportError as exc:
        raise ImportError('Install polars to load the Foursquare dataset: pip install polars') from exc

    catalog = get_foursquare_catalog()
    table = catalog.load_table(('datasets', 'places_os'))
    return pl.scan_iceberg(table).limit(limit).collect()
