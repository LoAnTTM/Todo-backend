from pydantic import BaseModel, Field
from pydantic.v1 import ConfigDict
from typing import Optional

class TodoBase(BaseModel):
    """
    Schema Pydantic cơ sở cho một Todo.
    """
    title: str
    done: bool = False

class TodoCreate(BaseModel):
    """
    Schema Pydantic cho việc tạo mới một Todo.
    """
    #Guideline: not null (min_length=1) và <= 140 ký tự
    title: str = Field(..., min_length=1, max_length=140, description="Tiêu đề không được rỗng và phải ít hơn 140 ký tự")

class TodoUpdate(BaseModel):
    """
    Schema Pydantic cho việc cập nhật một Todo.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=140, description="Tiêu đề mới (tùy chọn)")
    done: Optional[bool] = Field(None, description="Trạng thái hoàn thành mới (tùy chọn)")

class Todo(TodoBase):
    """
    Schema Pydantic đầy đủ cho một Todo (dùng cho response).
    """
    id: int

    #config Pydantic
    model_config = ConfigDict(from_attributes=True)

