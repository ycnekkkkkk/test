# IELTS Test - FastAPI + Next.js với Gemini AI

Hệ thống test IELTS đơn giản với AI, hỗ trợ 5-10 người dùng đồng thời.

## 🚀 Cài đặt

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
```

Tạo file `.env`:
```env
DATABASE_URL=sqlite:///./test_session.db
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY_BACKUP=your_backup_gemini_api_key_here
```

**Lưu ý về API Keys:**
- `GEMINI_API_KEY`: Key chính (bắt buộc)
- `GEMINI_API_KEY_BACKUP`: Key dự phòng (khuyến nghị để tránh rate limit)
- Hệ thống tự động chuyển đổi giữa 2 keys:
  - Nếu key 1 vừa được dùng (< 5 phút), tự động chuyển sang key 2
  - Nếu từ 5 phút trở lên, dùng lại key 1
  - Giúp tránh vượt quá rate limit khi tạo nhiều bài test liên tiếp

Chạy backend:
```bash
uvicorn app.main:app --reload
```

API sẽ chạy tại: http://localhost:8000

### Frontend (Next.js)

```bash
cd frontend
npm install
```

Tạo file `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Chạy frontend:
```bash
npm run dev
```

Frontend sẽ chạy tại: http://localhost:3000

## 📋 Flow

1. **Khởi tạo**: User chọn level (Beginner → Advanced) → Tạo test_session
2. **Chọn phần**: User chọn phase (Listening & Speaking HOẶC Reading & Writing)
3. **Generate**: Hệ thống gọi Gemini API 1 lần để tạo đề cho phase đã chọn
4. **Làm bài**: User làm bài trong 30 phút
5. **Nộp phase 1**: AI chấm điểm và lưu kết quả
6. **Generate phase 2**: Hệ thống tạo đề cho phase còn lại
7. **Làm và nộp phase 2**: User làm và nộp phase 2
8. **Tổng hợp**: Tính IELTS equivalent (Listening, Reading, Writing, Speaking, Overall)

## 🔧 API Endpoints

- `POST /api/sessions` - Tạo session mới
- `POST /api/sessions/{id}/select-phase` - Chọn phase
- `POST /api/sessions/{id}/generate` - Generate phase 1
- `POST /api/sessions/{id}/submit-phase1` - Nộp phase 1
- `POST /api/sessions/{id}/generate-phase2` - Generate phase 2
- `POST /api/sessions/{id}/submit-phase2` - Nộp phase 2
- `POST /api/sessions/{id}/aggregate` - Tổng hợp kết quả
- `GET /api/sessions/{id}` - Lấy thông tin session

## 📝 Ghi chú

- Sử dụng Gemini API free tier
- Tối ưu cho 5-10 người dùng đồng thời
- Mỗi phase chỉ gọi AI 1 lần (không regenerate)
- Scoring tự động cho Listening/Reading (objective)
- Scoring bằng AI cho Speaking/Writing (subjective)

