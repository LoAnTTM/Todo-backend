from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os # Thêm thư viện 'os'

raw_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173")

origins = [origin.strip() for origin in raw_origins.split(",")]


def setup_cors(app: FastAPI):
    """
    Thêm CORSMiddleware vào ứng dụng FastAPI.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,       # Sử dụng biến 'origins' đã đọc
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print(f"Đã cấu hình CORS cho phép origin: {', '.join(origins)}")

