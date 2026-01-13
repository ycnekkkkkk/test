# Hướng dẫn Deploy lên Railway

## 📋 Yêu cầu
- Tài khoản Railway: https://railway.app
- GitHub repository đã push code

## 🚀 Deploy Backend (FastAPI)

### Bước 1: Tạo Service mới
1. Đăng nhập Railway: https://railway.app
2. Click "New Project"
3. Chọn "Deploy from GitHub repo"
4. Chọn repository: `ycnekkkkkk/AItest`
5. Chọn "Add Service" → "GitHub Repo"

### Bước 2: Cấu hình Backend Service
1. Trong service vừa tạo, click "Settings"
2. Đặt tên service: `backend` (hoặc `ielts-backend`)
3. Trong tab "Source":
   - Root Directory: `backend`
   - Build Command: (để trống, Railway tự detect)
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Bước 3: Cấu hình Environment Variables
Trong tab "Variables", thêm:
```
DATABASE_URL=sqlite:///./test_session.db
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY_BACKUP=your_backup_gemini_api_key_here
PORT=8000
```

### Bước 4: Deploy
1. Railway sẽ tự động detect Python và cài đặt dependencies từ `requirements.txt`
2. Service sẽ tự động deploy khi có commit mới
3. Lấy URL từ tab "Settings" → "Domains" → "Generate Domain"

## 🎨 Deploy Frontend (Next.js)

### Bước 1: Tạo Service mới cho Frontend
1. Trong cùng project, click "New Service"
2. Chọn "GitHub Repo" → chọn lại repository `ycnekkkkkk/AItest`

### Bước 2: Cấu hình Frontend Service
1. Đặt tên service: `frontend` (hoặc `ielts-frontend`)
2. Trong tab "Source":
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm start`

### Bước 3: Cấu hình Environment Variables
Trong tab "Variables", thêm:
```
NEXT_PUBLIC_API_URL=https://your-backend-domain.railway.app
PORT=3000
NODE_ENV=production
```

**Lưu ý:** Thay `your-backend-domain.railway.app` bằng domain thực tế của backend service

### Bước 4: Deploy
1. Railway sẽ tự động detect Node.js và cài đặt dependencies
2. Service sẽ tự động deploy khi có commit mới
3. Lấy URL từ tab "Settings" → "Domains" → "Generate Domain"

## 🔧 Cập nhật CORS trong Backend

Sau khi có domain của Frontend, cần cập nhật CORS trong `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-domain.railway.app",  # Thêm domain Railway
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Sau đó commit và push lại code.

## 📝 Kiểm tra

1. Backend API: `https://your-backend-domain.railway.app/api/docs` (Swagger UI)
2. Frontend: `https://your-frontend-domain.railway.app`

## 🔄 Auto Deploy

Railway tự động deploy khi có commit mới vào branch `main`. 
Để deploy từ branch khác, vào Settings → Source → Branch.

## 💡 Tips

- Railway cung cấp free tier với giới hạn nhất định
- Database SQLite sẽ bị reset mỗi lần redeploy (nên dùng PostgreSQL cho production)
- Có thể thêm PostgreSQL service trong Railway và cập nhật `DATABASE_URL`

