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

## Endpoints

- `/api/webstore/orders/`
- `/api/warehouse/products/`
- `/api/warehouse/inventory/`
- `/api/marketing/customers/`
- `/api/marketing/campaigns/`
- `/api/transport/shipments/`
