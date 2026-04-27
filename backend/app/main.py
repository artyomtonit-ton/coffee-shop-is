from fastapi import FastAPI

app = FastAPI(
    title="Coffee Shop Information System",
    description="Diploma project: information system for a coffee shop",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
