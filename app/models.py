from sqlalchemy import Column, Integer, String, Boolean
from .db import Base


class Todo(Base):
    """
    Model SQLAlchemy đại diện cho một mục 'Todo' trong CSDL.
    """
    __tablename__ = "todos"

    #collum id
    id = Column(Integer, primary_key=True, index=True)

    #collum title
    title = Column(String(140), nullable=False, index=True)

    #collum trang thai, default false
    done = Column(Boolean, default=False, nullable=False)

