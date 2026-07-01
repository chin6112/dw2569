param(
    [string]$CsvPath = '.\downloads\foursquare_places_os_10k.csv'
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $CsvPath)) {
    $candidate = Get-ChildItem '.\downloads' -File -Filter '*.csv' -ErrorAction SilentlyContinue |
        Where-Object { $_.Length -gt 0 } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($null -ne $candidate) {
        $CsvPath = $candidate.FullName
        Write-Host "CSV path not found. Using latest non-empty CSV: $CsvPath"
    } else {
        Write-Error "CSV file not found or empty: $CsvPath"
    }
}

if ((Get-Item $CsvPath).Length -le 0) {
    Write-Error "CSV file is empty: $CsvPath"
}

$createSql = 'CREATE TABLE IF NOT EXISTS foursquare_places_os_sample (fsq_place_id String, name String, latitude Nullable(Float64), longitude Nullable(Float64), locality Nullable(String), region Nullable(String), country Nullable(String)) ENGINE = MergeTree() ORDER BY fsq_place_id'
$insertSql = 'INSERT INTO foursquare_places_os_sample FORMAT CSVWithNames'
$countSql = 'SELECT count() AS total_rows FROM foursquare_places_os_sample'
$topCountrySql = 'SELECT country, count() AS cnt FROM foursquare_places_os_sample GROUP BY country ORDER BY cnt DESC LIMIT 10'

Write-Host '[1/4] Creating ClickHouse table...'
& docker exec clickhouse-server clickhouse-client --query $createSql
if ($LASTEXITCODE -ne 0) {
    Write-Error 'Failed to create table in ClickHouse.'
}

Write-Host '[2/4] Loading CSV into ClickHouse...'
Get-Content $CsvPath | Where-Object { $_.Trim().Length -gt 0 } | docker exec -i clickhouse-server clickhouse-client --query $insertSql
if ($LASTEXITCODE -ne 0) {
    Write-Error 'Failed to insert CSV into ClickHouse.'
}

Write-Host '[3/4] Checking row count...'
& docker exec clickhouse-server clickhouse-client --query $countSql
if ($LASTEXITCODE -ne 0) {
    Write-Error 'Failed to check row count from ClickHouse.'
}

Write-Host '[4/4] Top countries...'
& docker exec clickhouse-server clickhouse-client --query $topCountrySql
if ($LASTEXITCODE -ne 0) {
    Write-Error 'Failed to query top countries from ClickHouse.'
}

Write-Host 'Done: Foursquare sample loaded and verified.'
