Init Alembic migrations: `alembic init migrations`<br>
Make first migration: `alembic revision --autogenerate -m 'Init'`<br>
Migrate all: `alembic upgrade head`

Run docker-compose.yml: `docker-compose up -d`

Run project: `uvicorn main:app --host localhost --port 8000 --reload`

Generate docs by Sphinx: `.\make.bat html`
