from pydantic import BaseModel, Field
from pydantic.v1 import ConfigDict
from typing import Optional

class TodoBase(BaseModel):
    """
    Base Pydantic schema for a Todo.
    """
    title: str
    done: bool = False

class TodoCreate(BaseModel):
    """
    Pydantic schema for creating a new Todo.
    """
    # Guideline: not null (min_length=1) and <= 140 characters
    title: str = Field(..., min_length=1, max_length=140, description="Title cannot be empty and must be fewer than 140 characters")

class TodoUpdate(BaseModel):
    """
    Pydantic schema for updating an existing Todo.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=140, description="New title (optional)")
    done: Optional[bool] = Field(None, description="Updated completion status (optional)")

class Todo(TodoBase):
    """
    Full Pydantic schema for a Todo (used for responses).
    """
    id: int

    # Pydantic configuration
    model_config = ConfigDict(from_attributes=True)
