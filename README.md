# 🚀 AI Face Analyzer (Hệ Thống Phân Tích Khuôn Mặt AI Đơn Trang & Mô-đun Hóa)

Hệ thống phân tích khuôn mặt trí tuệ nhân tạo chuyên nghiệp, hỗ trợ **ước lượng tuổi**, **phân tích cảm xúc** và **đánh giá điểm chất lượng hình ảnh**. 

Dự án được xây dựng với kiến trúc **Mô-đun hóa 1-to-1 (Multi-Page Modular Architecture)**: Mỗi tính năng chính sẽ bao gồm một mô-đun backend riêng biệt kết nối trực tiếp tới một tệp giao diện HTML độc lập. Toàn bộ CSS và JS bổ trợ được viết gọn gàng, đóng gói bên trong thẻ `<style>` và `<script>` của chính trang HTML đó, mang lại khả năng phân tách độc lập tuyệt vời!

---

## 🌟 Tính Năng Nổi Bật (Key Features)

1. **Kiến Trúc Mô-đun Tuyệt Đối (Modular Architecture)**:
   - Tệp khởi chạy `main.py` đặt ngoài thư mục gốc điều phối toàn hệ thống.
   - Các API Endpoint được chia tách thành các APIRouter chuyên biệt: `scanner.py`, `history.py`, `analytics.py`.
   - Các trang Frontend độc lập tương ứng: `scanner.html`, `history.html`, `analytics.html` với mã CSS/JS đóng gói trọn vẹn bên trong tệp.
2. **AI Facial Scanning & Analytics**:
   - **Ước lượng tuổi (Age Estimation)**: Dự đoán độ tuổi khuôn mặt dựa trên mạng thần kinh hoặc cấu trúc nếp nhăn biểu bì da.
   - **Phân tích cảm xúc (Emotion Analysis)**: Phân tách chi tiết trọng số cảm xúc (Vui vẻ, Bình thường, Buồn bã, Ngạc nhiên, Giận dữ, Sợ hãi) hiển thị bằng thanh tiến trình neon rực rỡ.
3. **Image Quality Scoring (Đánh Giá Chất Lượng Ảnh)**:
   - Tự động chấm điểm chất lượng hình ảnh (0 - 100%) dựa trên OpenCV: Độ sắc nét (Laplacian variance), Độ sáng (Luminance), Độ tương phản (StdDev), và Độ phân giải ảnh.
4. **Live AI Webcam & Shutter Flash**:
   - Tích hợp webcam live, lưới căn chỉnh tỷ lệ, hiệu ứng chớp sáng chụp ảnh (shutter flash) và tia quét laser.
5. **Database Auto-Fallback**:
   - Tự động kết nối tới **PostgreSQL**. Nếu database chưa được khởi tạo, hệ thống tự động chuyển đổi dự phòng sang **SQLite cục bộ** (`backend/face_analysis.db`) và hiển thị trực quan trạng thái trên giao diện.

---

## 📂 Cấu Trúc Thư Mục Mô-đun (Folder Structure)

```
d:/Xâm/xAI/
├── main.py                     # [ROOT] Điểm khởi chạy & Định tuyến trang chính
├── backend/
│   ├── database.py             # Kết nối PostgreSQL / SQLite dự phòng
│   ├── models.py               # Khai báo bảng cơ sở dữ liệu SQLAlchemy
│   ├── schemas.py              # Định nghĩa kiểu dữ liệu Pydantic
│   ├── scanner.py              # [MÔ-ĐUN SCANNER] Backend giải thuật AI & Router quét ảnh
│   ├── history.py              # [MÔ-ĐUN HISTORY] Backend Router lấy/xóa lịch sử
│   ├── analytics.py            # [MÔ-ĐUN ANALYTICS] Backend Router tổng hợp biểu đồ
│   └── requirements.txt        # Các thư viện Python cần thiết
├── frontend/
│   ├── scanner.html            # [MÔ-ĐUN SCANNER] Giao diện quét ảnh & webcam live
│   ├── history.html            # [MÔ-ĐUN HISTORY] Giao diện bảng nhật ký
│   └── analytics.html          # [MÔ-ĐUN ANALYTICS] Giao diện biểu đồ thống kê
├── uploads/                    # Thư mục chứa hình ảnh quét (lưu ngoài gốc)
└── README.md                   # Hướng dẫn sử dụng
```

---

## 🛠️ Hướng Dẫn Cài Đặt & Chạy Ứng Dụng (Setup Guide)

### Bước 1: Chuẩn bị môi trường Python
Yêu cầu hệ điều hành đã cài đặt Python 3.8 trở lên. Mở Terminal tại thư mục dự án và thực hiện:

```bash
# Tạo môi trường ảo (Khuyên dùng)
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Trên Windows (CMD):
.\venv\Scripts\activate.bat
```

### Bước 2: Cài đặt các thư viện phụ thuộc
Cài đặt toàn bộ dependencies trong file `backend/requirements.txt`:

```bash
pip install -r backend/requirements.txt
```

*Lưu ý: Thư viện `deepface` (bao gồm TensorFlow) có kích thước khá nặng. Bộ code đã được lập trình cơ chế dự phòng thông minh nên ứng dụng vẫn hoạt động mượt mà bằng OpenCV ngay cả khi bạn chưa cài đặt `deepface`.*

### Bước 3: Cấu hình Database (PostgreSQL)
Mặc định hệ thống kết nối tới PostgreSQL theo chuỗi URI:
`postgresql://postgres:postgres@localhost:5432/face_analysis`

Bạn có thể chỉnh sửa chuỗi kết nối bằng cách tạo tệp `.env` trong thư mục gốc hoặc cấu hình biến môi trường:
```env
DATABASE_URL=postgresql://user:password@host:port/database_name
```
*Nếu bạn chưa khởi tạo PostgreSQL, hệ thống sẽ tự động chuyển sang **SQLite Fallback** và lưu cơ sở dữ liệu dạng tệp tệp tin tại `backend/face_analysis.db` để bạn trải nghiệm ngay lập tức.*

### Bước 4: Khởi chạy FastAPI Backend
Chạy lệnh uvicorn từ thư mục gốc để bật máy chủ API và phục vụ trang web:

```bash
uvicorn main:app --reload
```
Sau khi khởi động thành công:
- Tài liệu API tự động (Swagger UI) sẽ có mặt tại: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Thư mục lưu ảnh phân tích sẽ được ánh xạ tại: [http://127.0.0.1:8000/uploads/](http://127.0.0.1:8000/uploads/)

### Bước 5: Trải nghiệm Giao Diện Frontend (Qua Link Web)
Giờ đây, bạn không cần mở tệp thủ công hay dùng Live Server nữa. Khi máy chủ FastAPI đang chạy, chỉ cần mở trình duyệt và truy cập trực tiếp bằng đường link web:

👉 **[http://localhost:8000/](http://localhost:8000/)** hoặc **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

*Lưu ý: Nếu không chạy máy chủ, bạn vẫn có thể nhấp đúp chuột trực tiếp vào tệp `frontend/scanner.html` để mở ở dạng offline (hệ thống sẽ tự động chuyển hướng kết nối ngoại vi an toàn).*

---

## 📈 Nguyên Lý Hoạt Động Của Giao Diện Mô-Đun

- **Độc lập tương đối (Self-Contained Files)**: 
  Tất cả kiểu dáng giao diện và lô-gíc xử lý JS của một trang đều nằm trọn vẹn trong trang đó. Bạn có thể thay đổi thiết kế của mô-đun Lịch Sử trong `history.html` mà hoàn toàn không ảnh hưởng hay làm vỡ giao diện của mô-đun Quét ảnh `scanner.html`.
- **Chuyển trạng thái giữa các trang (Cross-page Data Handling)**:
  Khi bạn đang ở trang Lịch Sử (`/history`) và muốn xem lại một ảnh quét cũ, hệ thống sẽ lưu thông tin bản ghi đó vào bộ nhớ đệm `sessionStorage` của trình duyệt và chuyển hướng bạn về `/scanner`. Trang Quét ảnh khi tải lên sẽ tự động phát hiện khóa bộ nhớ này và kết xuất kết quả cũ ngay lập tức mà không cần máy chủ quét lại!
- **Thanh điều hướng Sidebar thông minh**:
  Cả 3 trang `scanner.html`, `history.html`, `analytics.html` đều dựng chung thiết kế Sidebar. Khi nhấp vào các liên kết điều hướng, hệ thống sẽ thực hiện tải trang theo các đường dẫn URL cực kỳ chuyên nghiệp và trực quan.
