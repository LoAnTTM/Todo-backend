from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import todos
from .core.cors import setup_cors
from .db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle application startup and shutdown events.
    """
    print("Application starting...")
    # Create database tables (if they do not exist) during startup
    create_db_and_tables()
    yield
    # (Add cleanup logic here if needed)
    print("Application shutting down...")

# Create the FastAPI application instance
app = FastAPI(
    title="Todo List API",
    description="API for the Todo List application.",
    version="1.0.0",
    lifespan=lifespan # Attach lifespan manager to the app
)

# Configure CORS
setup_cors(app)

# Register router (API endpoints) for /todos
app.include_router(todos.router)

# Root route for API health check
@app.get("/", tags=["Root"], summary="API health check")
def read_root():
    """
    Quick route to verify whether the API is running.
    """
    return {"message": "Welcome to the Todo List API!"}
