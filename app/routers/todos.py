from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..db import get_db

# Khởi tạo router
router = APIRouter(
    prefix="/todos",  # Tất cả API trong file này sẽ có tiền tố /todos
    tags=["Todos"]  # Nhóm các API này vào nhóm "Todos" trong docs
)


# === 1. GET /todos ===
@router.get("/", response_model=List[schemas.Todo], summary="Lấy danh sách tất cả Todos")
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lấy về một danh sách các todo.
    """
    todos = db.query(models.Todo).offset(skip).limit(limit).all()
    return todos


# === 2. POST /todos ===
@router.post("/", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED, summary="Tạo một Todo mới")
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """
    Tạo một todo mới.
    - **title**: Tiêu đề của todo (bắt buộc, <= 140 ký tự).
    """
    # Tạo model SQLAlchemy từ schema Pydantic
    db_todo = models.Todo(title=todo.title)

    # Thêm vào session
    print(db_todo)

    db.add(db_todo)

    print(db_todo)

    # --- DÒNG QUAN TRỌNG NHẤT ---
    # Commit (lưu) thay đổi vào CSDL
    db.commit()
    # -----------------------------

    # Làm mới (refresh) db_todo để lấy ID vừa được CSDL tạo ra
    db.refresh(db_todo)

    # Trả về đối tượng vừa tạo
    return db_todo


# === 3. PATCH /todos/{id} ===
@router.patch("/{id}", response_model=schemas.Todo, summary="Cập nhật một Todo")
def update_todo(id: int, todo_update: schemas.TodoUpdate, db: Session = Depends(get_db)):
    """
    Cập nhật một todo đã tồn tại bằng ID.
    Bạn có thể cập nhật `title` hoặc `done` (hoặc cả hai).
    """
    # Tìm todo trong CSDL
    db_todo = db.query(models.Todo).get(id)

    # Nếu không tìm thấy, báo lỗi 404
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")

    # Lấy dữ liệu từ Pydantic model (chỉ lấy các trường đã được gửi lên)
    update_data = todo_update.dict(exclude_unset=True)

    # Cập nhật từng trường
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    # Thêm vào session (để đánh dấu là đã thay đổi)
    db.add(db_todo)

    # --- DÒNG QUAN TRỌNG ---
    # Commit thay đổi
    db.commit()
    # -----------------------

    # Làm mới để lấy dữ liệu mới nhất
    db.refresh(db_todo)

    # Trả về todo đã cập nhật
    return db_todo


# === 4. DELETE /todos/{id} ===
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Xóa một Todo")
def delete_todo(id: int, db: Session = Depends(get_db)):
    """
    Xóa một todo bằng ID.
    """
    db_todo = db.query(models.Todo).get(id)

    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")

    db.delete(db_todo)

    # --- DÒNG QUAN TRỌNG ---
    # Commit thay đổi
    db.commit()
    # -----------------------

    # Trả về status 204 (No Content)
    return

