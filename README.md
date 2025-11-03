# Flow Manager (MySQL) - FastAPI (MVC)

This repository contains the Flow Manager microservice implemented in FastAPI using a MySQL database. The project uses MVC-like separation with repositories and services.

## Features
- FastAPI + asyncio flow orchestration
- MySQL as the primary database (MySQL 8)
- SQL schema and seed files provided in `sql/` and executed on DB initialization
- Swagger UI available at `/docs`
- Docker Compose to bring up MySQL and the app
- Makefile target for easy initialization

## Quickstart (Docker Compose)

1. Build and start the services:
```bash
make build-and-start
```

2. Swagger UI: `http://localhost:8000/docs`

## Local development (no Docker)

3. Ensure you have a MySQL server and create a database named `flowdb` and a user `flowuser` with password `flowpass`, or set `DATABASE_URL` accordingly:
```bash
export DATABASE_URL='mysql+pymysql://flowuser:flowpass@localhost:3306/flowdb'
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Start server:
```bash
uvicorn app.main:app --reload
```

## Notes
- The MySQL container will execute `sql/schema.sql` and `sql/seed.sql` when creating the database volume for the first time (via `/docker-entrypoint-initdb.d`). The app also performs checks on startup to ensure tables exist and seeds the `tasks` if necessary.
