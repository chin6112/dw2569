# Django Platform for Silo Systems

This workspace contains a Django project configured for multiple silo systems:
- `webstore`
- `warehouse`
- `marketing`
- `transport`

## Setup

1. Create a virtual environment:

   python -m venv .venv

2. Activate it:

   .venv\Scripts\Activate.ps1  # PowerShell
   .venv\Scripts\activate.bat  # Command Prompt

3. Install dependencies:

   pip install -r requirements.txt

4. Run migrations:

   python manage.py migrate

5. Run development server with uvicorn:

   uvicorn config.asgi:application --reload

## Run With Docker Compose

Start Django + ClickHouse with one command:

```bash
docker compose up --build
```

Services:
- Django web app: `http://localhost:8000/sales/`
- ClickHouse HTTP: `http://localhost:8123`

Open a second terminal for management commands:

```bash
docker compose exec web python manage.py generate_sale --count 100
docker compose exec web python manage.py clickhouse_sync_orders
```

## ClickHouse Integration

This project supports ClickHouse as a separate analytics store. Install a ClickHouse server and configure connection settings with environment variables:

- `CLICKHOUSE_HOST` (default: `localhost`)
- `CLICKHOUSE_PORT` (default: `8123`)
- `CLICKHOUSE_USER` (default: `default`)
- `CLICKHOUSE_PASSWORD`
- `CLICKHOUSE_DB` (default: `default`)

After setting the environment, ensure the ClickHouse server is running and reachable on the configured host/port.
For a local ClickHouse server you can use the default HTTP port `8123`.

Then sync orders into ClickHouse with:

```bash
python manage.py clickhouse_sync_orders
```

Using Docker Compose, run:

```bash
docker compose exec web python manage.py clickhouse_sync_orders
```

## Foursquare Example Dataset

Run the example query through the ClickHouse container:

```bash
docker exec clickhouse-server clickhouse-client --query="SELECT * FROM s3('s3://fsq-os-places-us-east-1/release/dt=2025-04-08/places/parquet/*') LIMIT 1"
```

## Demo Deliverables Guide

For all requested deliverables (GitHub repo link, `docker compose up` video flow, website screenshot checklist, and Foursquare query demo video), use:

- [docs/CLICKHOUSE_DEMO_GUIDE.md](docs/CLICKHOUSE_DEMO_GUIDE.md)

## Endpoints

- `/api/webstore/orders/`
- `/api/warehouse/products/`
- `/api/warehouse/inventory/`
- `/api/marketing/customers/`
- `/api/marketing/campaigns/`
- `/api/transport/shipments/`
