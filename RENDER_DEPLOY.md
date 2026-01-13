# Hướng dẫn Deploy Backend lên Render

## 📋 Yêu cầu
- Tài khoản Render: https://render.com (Free tier có sẵn)
- GitHub repository đã push code

## 🚀 Deploy Backend (FastAPI) lên Render

### Bước 1: Tạo Account và Connect GitHub
1. Đăng ký/Đăng nhập Render: https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub account nếu chưa
4. Chọn repository: `ycnekkkkkk/AItest`

### Bước 2: Cấu hình Service
1. **Name**: `ielts-backend` (hoặc tên bạn muốn)
2. **Region**: Singapore (sin) hoặc gần nhất
3. **Branch**: `main`
4. **Root Directory**: `backend`
5. **Runtime**: `Python 3`
6. **Build Command**: `pip install -r requirements.txt`
7. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Bước 3: Environment Variables
Trong phần "Environment Variables", thêm:
```
DATABASE_URL=sqlite:///./test_session.db
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY_BACKUP=your_backup_gemini_api_key_here
FRONTEND_URL=https://your-frontend-domain.vercel.app
PORT=10000
```

**Lưu ý:** 
- Thay `your_gemini_api_key_here` bằng API key thực tế
- Thay `your-frontend-domain.vercel.app` bằng domain Vercel của bạn
- Render free tier sử dụng port 10000

### Bước 4: Chọn Plan
- Chọn **Free** plan (đủ dùng cho development)
- Free tier có giới hạn:
  - Service sẽ sleep sau 15 phút không có traffic
  - Wake up mất vài giây khi có request mới
  - 750 giờ/tháng

### Bước 5: Deploy
1. Click "Create Web Service"
2. Render sẽ tự động build và deploy
3. Đợi build xong (khoảng 2-5 phút)
4. Lấy URL từ dashboard: `https://ielts-backend.onrender.com` (hoặc tên bạn đặt)

### Bước 6: Custom Domain (Tùy chọn)
1. Vào Settings → Custom Domains
2. Thêm domain nếu có

## 🔧 Cập nhật Frontend

Sau khi có backend URL từ Render, cập nhật environment variable trong Vercel:

1. Vào Vercel Dashboard → Project → Settings → Environment Variables
2. Cập nhật `NEXT_PUBLIC_API_URL`:
   ```
   NEXT_PUBLIC_API_URL=https://ielts-backend.onrender.com
   ```
3. Redeploy frontend để áp dụng thay đổi

## 🔄 Auto Deploy

Render tự động deploy khi có commit mới vào branch `main`.
- Manual Deploy: Có thể trigger manual từ dashboard
- Auto Deploy: Tự động khi push code

## 📝 Kiểm tra

1. Backend API: `https://ielts-backend.onrender.com/api/docs` (Swagger UI)
2. Health Check: `https://ielts-backend.onrender.com/health`
3. Frontend: `https://your-project.vercel.app`

## ⚠️ Lưu ý về Free Tier

- **Sleep Mode**: Service sẽ sleep sau 15 phút không có traffic
- **Cold Start**: Lần đầu sau khi sleep, request đầu tiên sẽ mất 30-60 giây để wake up
- **Database**: SQLite sẽ bị reset mỗi lần redeploy (nên dùng PostgreSQL cho production)

## 💡 Upgrade lên Paid Plan (Nếu cần)

Nếu cần service chạy 24/7 không sleep:
- Starter Plan: $7/tháng
- Không bị sleep, performance tốt hơn

## 🔗 Liên kết

- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs
- Python on Render: https://render.com/docs/deploy-python

