from fastapi import FastAPI

from app.config import settings


app = FastAPI(
    title=settings.app_name,
    description="Diploma project: information system for a coffee shop",
    version=settings.app_version,
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
