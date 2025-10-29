from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..db import get_db

# Tạo một APIRouter mới
router = APIRouter(
    prefix="/todos",  # Tiền tố cho tất cả các route trong router này
    tags=["Todos"],  # Tag để nhóm các API trong tài liệu Swagger
)


@router.get(
    "/",
    response_model=List[schemas.Todo],
    summary="Lấy danh sách tất cả Todos"
)
def get_all_todos(db: Session = Depends(get_db)):
    """
    Lấy danh sách tất cả các mục công việc.
    """
    todos = db.query(models.Todo).all()
    return todos


@router.post(
    "/",
    response_model=schemas.Todo,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo một Todo mới"
)
def create_todo(
        todo_create: schemas.TodoCreate,
        db: Session = Depends(get_db)
):
    """
    Tạo một mục công việc mới.

    - **title**: Tiêu đề của công việc (bắt buộc, 1-140 ký tự).
    """
    # FastAPI đã tự động validate 'todo_create' dựa trên schema TodoCreate
    # Nếu validation thất bại, client sẽ nhận lỗi 422 Unprocessable Entity

    # Tạo đối tượng model SQLAlchemy
    new_todo = models.Todo(title=todo_create.title)

    # Thêm vào session CSDL
    db.add(new_todo)
    # Commit thay đổi
    db.commit()
    # Refresh để lấy ID đã được CSDL tạo
    db.refresh(new_todo)

    # Trả về đối tượng đã tạo
    return new_todo


@router.patch(
    "/{id}",
    response_model=schemas.Todo,
    summary="Cập nhật một Todo"
)
def update_todo(
        id: int,
        todo_update: schemas.TodoUpdate,
        db: Session = Depends(get_db)
):
    """
    Cập nhật tiêu đề hoặc trạng thái hoàn thành của một công việc.

    - **id**: ID của công việc cần cập nhật.
    - **title** (tùy chọn): Tiêu đề mới.
    - **done** (tùy chọn): Trạng thái hoàn thành mới.
    """
    # 1. Tìm todo trong CSDL
    db_todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    # 2. Nếu không tìm thấy, trả về lỗi 404
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # 3. Lấy dữ liệu cập nhật từ Pydantic model
    # exclude_unset=True nghĩa là chỉ lấy các trường đã được client gửi lên
    update_data = todo_update.model_dump(exclude_unset=True)

    # 4. Cập nhật các trường
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    # 5. Commit và refresh
    db.commit()
    db.refresh(db_todo)

    return db_todo


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa một Todo"
)
def delete_todo(id: int, db: Session = Depends(get_db)):
    """
    Xóa một mục công việc dựa trên ID.

    - **id**: ID của công việc cần xóa.
    """
    # 1. Tìm todo
    db_todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    # 2. Nếu không tìm thấy, trả về lỗi 404
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # 3. Xóa và commit
    db.delete(db_todo)
    db.commit()

    # 4. Trả về status 204 (No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

