from fastapi import FastAPI
from app.routes.sos import router as sos_router

app = FastAPI()
app.include_router(sos_router)


@app.get("/health")
def health():
    return {"status": "ok"}