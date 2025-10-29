# **Todo List Backend (FastAPI)**

Đây là phần backend cho ứng dụng Todo List, được xây dựng bằng FastAPI và PostgreSQL theo guideline đã cung cấp.

## **Công việc đã làm**

1. **Cấu trúc dự án**: Tuân thủ cấu trúc thư mục app/, app/routers, app/core v.v.  
2. **Database**:  
   * Tách biệt models.py (SQLAlchemy models) và schemas.py (Pydantic models).  
   * Sử dụng app/db.py để quản lý engine, SessionLocal và dependency get\_db.  
   * Tự động tạo bảng CSDL khi ứng dụng khởi động (sử dụng lifespan).  
3. **API Endpoints**:  
   * GET /todos: Lấy danh sách todos.  
   * POST /todos: Tạo todo mới (với validation: 1-140 ký tự).  
   * PATCH /todos/{id}: Cập nhật todo (title hoặc done).  
   * DELETE /todos/{id}: Xóa todo.  
4. **Error Handling**:  
   * Tự động trả về 422 Unprocessable Entity cho validation (nhờ Pydantic).  
   * Trả về 404 Not Found khi PATCH hoặc DELETE một id không tồn tại.  
5. **Status Codes**:  
   * 200 OK (cho GET, PATCH)  
   * 201 Created (cho POST)  
   * 204 No Content (cho DELETE)  
6. **CORS**: Cấu hình cho phép http://localhost:5173 (Vite dev server) truy cập.

## **Hướng dẫn cài đặt và chạy**

### **1\. Yêu cầu**

* Python 3.8+(Python 3.14.0)
* Một CSDL PostgreSQL đang chạy.

### **2\. Cài đặt**

1. Tạo môi trường ảo (khuyến nghị):  
   python \-m venv venv  
   source venv/bin/activate  \# Trên Windows: venv\\Scripts\\activate

2. Cài đặt các thư viện yêu cầu:  
   pip install \-r requirements.txt

### **3\. Cấu hình CSDL**

Trước khi chạy, bạn **BẮT BUỘC** phải cấu hình CSDL.

Mở tệp app/db.py và tìm dòng sau:

DATABASE\_URL \= os.environ.get("DATABASE\_URL", "postgresql://user:password@localhost/tododb")

Thay đổi chuỗi "postgresql://user:password@localhost/tododb" thành chuỗi kết nối (connection string) PostgreSQL của bạn.

Ví dụ: Nếu username là postgres, mật khẩu là admin, và database tên todo\_app, chuỗi sẽ là:  
"postgresql://postgres:admin@localhost:5432/todo\_app"

### **4\. Chạy ứng dụng (Dev)**

Chạy lệnh sau từ thư mục gốc todo-backend:

uvicorn app.main:app \--reload \--port 8000

### **5\. Kiểm tra API**

Truy cập [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs) để xem tài liệu và thử nghiệm API.