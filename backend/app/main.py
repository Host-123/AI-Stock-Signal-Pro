from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import test_connection
from app.services.stock_service import (
    get_stock_price,
    get_watchlist,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    test_connection()

    yield

    # Future:
    # Close database
    # Stop background scheduler
    # Release resources


app = FastAPI(
    title="AI Stock Signal Pro",
    description="Professional AI Powered Stock Analysis Platform",
    version="2.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------


@app.get("/", tags=["System"])
def home():
    return {
        "status": "running",
        "project": "AI Stock Signal Pro",
        "version": "2.0.0",
    }


@app.get("/health", tags=["System"])
def health():
    return {
        "success": True,
        "message": "Server is healthy",
    }


# ---------------------------------------------------------------------
# Stock APIs
# ---------------------------------------------------------------------


@app.get("/api/stock/{symbol}", tags=["Stock"])
def stock(symbol: str):
    return get_stock_price(f"{symbol}.NS")


@app.get("/api/watchlist", tags=["Watchlist"])
def watchlist():
    return get_watchlist()