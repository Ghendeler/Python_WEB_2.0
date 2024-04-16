import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from src.conf.config import settings
from src.routes import auth, contacts, users

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix='/api')

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    This function is run at the start of the application.
    It initializes the FastAPILimiter with a Redis instance.
    """
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    """
    This function is the root endpoint of the application.
    It returns a simple message.
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    """
    This is the main entry point of the application.
    It runs the FastAPI application with uvicorn.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)
