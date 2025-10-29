from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import todos
from .core.cors import setup_cors
from .db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager để xử lý các sự kiện khởi động và tắt ứng dụng.
    """
    print("Ứng dụng đang khởi động...")
    # Tạo bảng CSDL (nếu chúng chưa tồn tại) khi khởi động
    create_db_and_tables()
    yield
    # (Có thể thêm code dọn dẹp ở đây nếu cần)
    print("Ứng dụng đang tắt...")

# Tạo đối tượng ứng dụng FastAPI
app = FastAPI(
    title="Todo List API",
    description="API cho ứng dụng Todo List theo guideline.",
    version="1.0.0",
    lifespan=lifespan # Gắn lifespan vào ứng dụng
)

# Cấu hình CORS
setup_cors(app)

# Thêm router (API endpoints) cho /todos
app.include_router(todos.router)

# Thêm route gốc để kiểm tra API
@app.get("/", tags=["Root"], summary="Kiểm tra API hoạt động")
def read_root():
    """
    Route gốc để kiểm tra nhanh API có đang chạy hay không.
    """
    return {"message": "Chào mừng bạn đến với Todo List API!"}

