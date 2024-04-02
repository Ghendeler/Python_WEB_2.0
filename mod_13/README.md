Init Alembic migrations: `alembic init migrations`
`alembic revision --autogenerate -m 'Init'`
`alembic upgrade head`

Run project: `uvicorn main:app --host localhost --port 8000 --reload`
