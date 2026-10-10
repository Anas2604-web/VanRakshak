from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config.database import connect, close
from app.routes.sos import router as sos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await close()


app = FastAPI(lifespan=lifespan)
app.include_router(sos_router)

