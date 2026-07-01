import argparse
import subprocess
import sys
from pathlib import Path


def build_query(limit: int, fmt: str) -> str:
    return f"""
    SELECT
        fsq_place_id,
        name,
        latitude,
        longitude,
        address,
        locality,
        region,
        postcode,
        country,
        date_created,
        date_refreshed,
        fsq_category_labels
    FROM s3('s3://fsq-os-places-us-east-1/release/dt=2025-04-08/places/parquet/*')
    WHERE address IS NOT NULL
      AND postcode IS NOT NULL
      AND country IS NOT NULL
    LIMIT {limit}
    FORMAT {fmt}
    """.strip()


def download_foursquare(output_path: str, limit: int = 1000, fmt: str = 'CSVWithNames') -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    query = build_query(limit, fmt)
    cmd = ['clickhouse-client', '--query', query]

    with output.open('wb') as fh:
        completed = subprocess.run(cmd, stdout=fh, stderr=sys.stderr, check=True)

    if completed.returncode != 0:
        raise RuntimeError(f'Failed to download dataset. Exit code: {completed.returncode}')

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download a sample of the Foursquare Places dataset via ClickHouse.')
    parser.add_argument('--output', default='downloads/foursquare_places_sample.csv', help='Output file path')
    parser.add_argument('--limit', type=int, default=1000, help='Number of rows to download')
    parser.add_argument('--format', default='CSVWithNames', choices=['CSVWithNames', 'Parquet'], help='Output format')
    args = parser.parse_args()

    output_file = download_foursquare(args.output, limit=args.limit, fmt=args.format)
    print(f'Download complete: {output_file}')
