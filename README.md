# Products API (Azure Functions + Cosmos DB)

## Overview
Simple HTTP CRUD API for `Products` using Azure Functions (Python) and Cosmos DB (SQL API).
Partition key: `/Id`

## Endpoints
- `POST /api/products` — create product (body: id, name, price)
- `GET /api/products` — list products
- `GET /api/products/{id}` — retrieve product
- `PUT /api/products/{id}` — update product
- `DELETE /api/products/{id}` — delete product

## Local run
1. Install tools: Python 3.10+, Azure Functions Core Tools, Azure CLI
2. Create virtual env: `python -m venv .venv && source .venv/bin/activate`
3. Install deps: `pip install -r requirements.txt`
4. Update `local.settings.json` with your Cosmos DB URI and KEY
5. Run: `func start`

## Notes
- Container name: `pro1`
- Database name: `productDB`
