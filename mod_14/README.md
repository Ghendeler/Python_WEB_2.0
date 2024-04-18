Init Alembic migrations: `alembic init migrations`
Make first migration: `alembic revision --autogenerate -m 'Init'`
Migrate all: `alembic upgrade head`

Run docker-compose.yml: `docker-compose up -d`

Run project: `uvicorn main:app --host localhost --port 8000 --reload`
