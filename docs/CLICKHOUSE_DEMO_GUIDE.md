# ClickHouse + Django Demo Guide

## GitHub Repository

https://github.com/chin6112/dw2569.git

## 1) Start Services (record this as Video #1)

Run from project root:

```bash
docker compose up --build
```

Expected result:
- Django app: http://localhost:8000/sales/
- ClickHouse HTTP: http://localhost:8123

## 2) Website Screenshot

Open these pages in browser and capture screenshots:
- http://localhost:8000/sales/
- http://localhost:8000/inventory/
- http://localhost:8000/marketing/
- http://localhost:8000/transportation/

Suggested screenshot filename:
- website-sales.png

## 3) Query Foursquare Dataset via clickhouse-client (record this as Video #2)

Use Foursquare as the dataset source and query through `clickhouse-client` with this reliable workflow.

### 3.1 Export sample rows from FSQ Spatial Desktop

In FSQ Spatial Desktop SQL editor, run:

```sql
COPY (
	SELECT fsq_place_id, name, latitude, longitude, locality, region, country
	FROM places.datasets.places_os
	WHERE country IS NOT NULL
	LIMIT 10000
) TO 'C:/Velvet/คลัง/dw2569/downloads/foursquare_places_os_10k.csv' (HEADER, DELIMITER ',');
```

### 3.2 Copy CSV into ClickHouse container

```bash
docker cp ./downloads/foursquare_places_os_10k.csv clickhouse-server:/tmp/foursquare_places_os_10k.csv
```

Quick path (recommended): run one script to create table, import CSV, and query verification:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\foursquare_to_clickhouse.ps1 -CsvPath .\downloads\foursquare_places_os_10k.csv
```

### 3.3 Create table in ClickHouse

```bash
docker exec clickhouse-server clickhouse-client --query="CREATE TABLE IF NOT EXISTS foursquare_places_os_sample (
	fsq_place_id String,
	name String,
	latitude Nullable(Float64),
	longitude Nullable(Float64),
	locality Nullable(String),
	region Nullable(String),
	country Nullable(String)
) ENGINE = MergeTree() ORDER BY fsq_place_id"
```

### 3.4 Load CSV into ClickHouse

```bash
docker exec clickhouse-server clickhouse-client --query="INSERT INTO foursquare_places_os_sample FORMAT CSVWithNames" < ./downloads/foursquare_places_os_10k.csv
```

### 3.5 Query with clickhouse-client (for video)

```bash
docker exec clickhouse-server clickhouse-client --query="SELECT country, count() AS cnt FROM foursquare_places_os_sample GROUP BY country ORDER BY cnt DESC LIMIT 10"
```

Optional direct S3 query from ClickHouse docs (date paths may change over time):

```bash
docker exec clickhouse-server clickhouse-client --query="SELECT * FROM s3('s3://fsq-os-places-us-east-1/release/dt=2025-04-08/places/parquet/*') LIMIT 1"
```

## 4) Sync Django Orders into ClickHouse

Generate sample sales data:

```bash
docker compose exec web python manage.py generate_sale --count 100
```

Sync to ClickHouse:

```bash
docker compose exec web python manage.py clickhouse_sync_orders
```

Validate in ClickHouse:

```bash
docker exec clickhouse-server clickhouse-client --query="SELECT count() FROM orders"
```

## 5) Suggested Demo Flow

1. Start with `docker compose up --build`.
2. Open `/sales/` in browser and show page load.
3. Run `generate_sale` + `clickhouse_sync_orders`.
4. Query `SELECT count() FROM orders` in ClickHouse.
5. Run the Foursquare query via clickhouse-client.
