from fastapi import FastAPI
from app.database.database import test_connection
app = FastAPI(
    title="AI Stock Signal Pro",
    version="1.0.0"
)
@app.on_event("startup")
def startup():
    test_connection()
@app.get("/")
def home():
    return {
        "status": "Running",
        "project": "AI Stock Signal Pro"
    }

