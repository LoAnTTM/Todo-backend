from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os  # Import os module

raw_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173")

origins = [origin.strip() for origin in raw_origins.split(",")]


def setup_cors(app: FastAPI):
    """
    Add CORSMiddleware to the FastAPI application.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,       # Use the parsed 'origins' list
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print(f"CORS configured to allow origins: {', '.join(origins)}")
