from sqlalchemy import Column, Integer, String, Boolean
from .db import Base


class Todo(Base):
    """
    SQLAlchemy model representing a Todo item in the database.
    """
    __tablename__ = "todos"

    # Column id
    id = Column(Integer, primary_key=True, index=True)

    # Column title
    title = Column(String(140), nullable=False, index=True)

    # Column completion status, default false
    done = Column(Boolean, default=False, nullable=False)
