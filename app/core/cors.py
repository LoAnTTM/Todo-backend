from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Theo guideline là http://localhost:5173 (cổng mặc định của Vite)
origins = [
    "http://localhost:5173",
]

def setup_cors(app: FastAPI):
    """
    Thêm CORSMiddleware vào ứng dụng FastAPI.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,       # Cho phép các origin trong danh sách
        allow_credentials=True,    # Cho phép gửi cookie (nếu có)
        allow_methods=["*"],       # Cho phép tất cả các phương thức (GET, POST, v.v.)
        allow_headers=["*"],       # Cho phép tất cả các header
    )
    print("Đã cấu hình CORS cho phép origin: http://localhost:5173")

