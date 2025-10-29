from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import todos
from .core.cors import setup_cors
from .db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Ứng dụng đang khởi động...")
    create_db_and_tables()
    yield
    print("Ứng dụng đang tắt...")

#tao fast api
app = FastAPI(
    title="Todo List API",
    description="API cho ứng dụng Todo List theo guideline.",
    version="1.0.0",
    lifespan=lifespan # Gắn lifespan vào ứng dụng
)

#config cors
setup_cors(app)

#add routes cho todo
app.include_router(todos.router)

#add route de check api
@app.get("/", tags=["Root"], summary="Kiểm tra API hoạt động")
def read_root():
    """
    Route gốc để kiểm tra nhanh API có đang chạy hay không.
    """
    return {"message": "Chào mừng bạn đến với Todo List API!"}

