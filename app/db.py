import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:1234@localhost:5432/tododb")

# creat engine
engine = create_engine(DATABASE_URL)

# create session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base cho models
Base = declarative_base()

# create db
def create_db_and_tables():
    """
    Tạo tất cả các bảng trong CSDL được định nghĩa bởi Base.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("Đã tạo bảng CSDL thành công.")
    except Exception as e:
        print(f"Lỗi khi tạo bảng CSDL: {e}")

# cho fastApi get db
def get_db():
    """
    Dependency: Cung cấp một phiên CSDL cho mỗi request,
    tự động đóng phiên sau khi request hoàn tất.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
