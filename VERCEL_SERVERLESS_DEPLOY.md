# Hướng dẫn Deploy Backend lên Vercel Serverless Functions

## 📋 Yêu cầu
- Tài khoản Vercel: https://vercel.com
- GitHub repository đã push code
- Database external (Vercel Postgres, Supabase, hoặc MongoDB)

## ⚠️ Lưu ý quan trọng

Vercel Serverless Functions có một số hạn chế:
1. **Không hỗ trợ SQLite** - File system là read-only
2. **Cần database external** - PostgreSQL, MongoDB, hoặc Supabase
3. **Timeout limit** - 10 giây (Hobby), 60 giây (Pro)
4. **Cold start** - Lần đầu có thể mất vài giây

## 🗄️ Bước 1: Setup Database

### Option A: Vercel Postgres (Khuyến nghị)
1. Vào Vercel Dashboard → Project → Storage
2. Click "Create Database" → "Postgres"
3. Chọn plan (Hobby free có 256MB)
4. Lấy connection string

### Option B: Supabase (Free tier tốt)
1. Đăng ký: https://supabase.com
2. Tạo project mới
3. Vào Settings → Database → Connection string
4. Copy connection string

### Option C: MongoDB Atlas (Free tier)
1. Đăng ký: https://www.mongodb.com/cloud/atlas
2. Tạo cluster free
3. Lấy connection string

## 🚀 Bước 2: Deploy Frontend + Backend lên Vercel

### Bước 2.1: Import Project
1. Đăng nhập Vercel: https://vercel.com
2. Click "Add New..." → "Project"
3. Import từ GitHub: Chọn repository `ycnekkkkkk/AItest`
4. Vercel sẽ tự động detect Next.js

### Bước 2.2: Cấu hình Project
1. **Root Directory**: `frontend`
2. **Framework Preset**: Next.js (tự động detect)
3. **Build Command**: `npm run build` (mặc định)
4. **Output Directory**: `.next` (mặc định)

### Bước 2.3: Environment Variables
Thêm các biến môi trường:

```
# Database
DATABASE_URL=postgresql://user:password@host:port/database
# Hoặc nếu dùng Supabase:
# DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres

# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY_BACKUP=your_backup_gemini_api_key_here

# Frontend URL (sẽ được set tự động)
NEXT_PUBLIC_API_URL=https://your-project.vercel.app
```

### Bước 2.4: Cấu hình Python Runtime
Vercel sẽ tự động detect Python files trong `api/` folder và sử dụng Python runtime.

### Bước 2.5: Deploy
1. Click "Deploy"
2. Vercel sẽ:
   - Build Next.js frontend
   - Install Python dependencies từ `api/requirements.txt`
   - Deploy serverless functions từ `api/` folder
3. Sau khi deploy xong, bạn sẽ có URL: `https://your-project.vercel.app`

## 🔧 Bước 3: Cập nhật Database Schema

Sau khi có database, cần tạo tables. Có 2 cách:

### Cách 1: Chạy migration script
Tạo file `scripts/init_db.py` và chạy một lần:

```python
from sqlalchemy import create_engine
from app.database import Base
from app.models.test_session import TestSession
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
print("Database tables created!")
```

### Cách 2: Tự động tạo khi deploy
Code đã có `Base.metadata.create_all()` trong `api/index.py`, sẽ tự động tạo tables.

## 📝 Bước 4: Kiểm tra

1. **Frontend**: `https://your-project.vercel.app`
2. **Backend API**: `https://your-project.vercel.app/api/sessions`
3. **Health Check**: `https://your-project.vercel.app/api/health`
4. **Swagger UI**: `https://your-project.vercel.app/api/docs` (nếu có)

## 🔄 Cấu trúc API Routes

Vercel sẽ tự động map các routes:
- `POST /api/sessions` → `api/index.py` (handler)
- `GET /api/sessions/{id}` → `api/index.py` (handler)
- Tất cả routes được xử lý bởi FastAPI app trong `api/index.py`

## ⚙️ Tùy chỉnh Routes (Nếu cần)

Nếu muốn tách routes thành các file riêng:

```
api/
  sessions/
    [id]/
      index.py  # GET /api/sessions/:id
    index.py    # POST /api/sessions
```

## 💡 Tips

1. **Database Connection Pooling**: Vercel serverless functions nên dùng connection pooling
2. **Environment Variables**: Set trong Vercel Dashboard → Settings → Environment Variables
3. **Logs**: Xem logs trong Vercel Dashboard → Deployments → Functions
4. **Cold Start**: Lần đầu request có thể mất 2-5 giây

## 🐛 Troubleshooting

### Lỗi: "Database connection failed"
- Kiểm tra `DATABASE_URL` trong Environment Variables
- Đảm bảo database cho phép connections từ Vercel IPs
- Với Supabase: Vào Settings → Database → Connection Pooling

### Lỗi: "Module not found"
- Kiểm tra `api/requirements.txt` có đủ dependencies
- Redeploy để cài lại dependencies

### Lỗi: "Timeout"
- Vercel Hobby plan có timeout 10 giây
- Upgrade lên Pro plan (60 giây) nếu cần
- Hoặc optimize code để chạy nhanh hơn

## 🔗 Liên kết

- Vercel Serverless Functions: https://vercel.com/docs/functions
- Vercel Python Runtime: https://vercel.com/docs/functions/runtimes/python
- Vercel Postgres: https://vercel.com/docs/storage/vercel-postgres

