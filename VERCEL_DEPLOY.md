# Hướng dẫn Deploy lên Vercel

## 📋 Yêu cầu
- Tài khoản Vercel: https://vercel.com
- GitHub repository đã push code
- Backend đã deploy (Railway/Render/hoặc Vercel Serverless)

## 🎨 Deploy Frontend (Next.js) lên Vercel

### Bước 1: Import Project
1. Đăng nhập Vercel: https://vercel.com
2. Click "Add New..." → "Project"
3. Import từ GitHub: Chọn repository `ycnekkkkkk/AItest`
4. Vercel sẽ tự động detect Next.js

### Bước 2: Cấu hình Project
1. **Root Directory**: Chọn `frontend`
2. **Framework Preset**: Next.js (tự động detect)
3. **Build Command**: `npm run build` (mặc định)
4. **Output Directory**: `.next` (mặc định)
5. **Install Command**: `npm install` (mặc định)

### Bước 3: Environment Variables
Thêm các biến môi trường:
```
NEXT_PUBLIC_API_URL=https://your-backend-domain.railway.app
```
**Lưu ý:** Thay `your-backend-domain.railway.app` bằng domain thực tế của backend

### Bước 4: Deploy
1. Click "Deploy"
2. Vercel sẽ tự động build và deploy
3. Sau khi deploy xong, bạn sẽ có URL: `https://your-project.vercel.app`

### Bước 5: Custom Domain (Tùy chọn)
1. Vào Project Settings → Domains
2. Thêm custom domain nếu có

## 🔧 Deploy Backend

Bạn có 2 lựa chọn:

### Option 1: Giữ Backend trên Railway (Khuyến nghị)
- Backend FastAPI hoạt động tốt trên Railway
- Dễ quản lý và scale
- Xem hướng dẫn trong `RAILWAY_DEPLOY.md`

### Option 2: Deploy Backend lên Vercel (Serverless Functions)
**Lưu ý:** Cần refactor code để chuyển từ FastAPI sang Vercel Serverless Functions

Nếu muốn dùng Vercel Serverless:
1. Tạo folder `api/` trong root
2. Convert FastAPI routes thành Vercel serverless functions
3. Cấu hình `vercel.json` để route requests

## 🔄 Auto Deploy

Vercel tự động deploy khi có commit mới vào branch `main`.
- Production: Từ branch `main`
- Preview: Từ các branch/PR khác

## 📝 Cập nhật CORS trong Backend

Sau khi có domain Vercel, cập nhật CORS trong `backend/app/main.py`:

```python
allowed_origins = [
    "http://localhost:3000",
    "https://your-project.vercel.app",  # Thêm domain Vercel
]
```

Hoặc set biến môi trường `FRONTEND_URL` trong Railway backend service.

## 🧪 Kiểm tra

1. Frontend: `https://your-project.vercel.app`
2. Backend API: `https://your-backend-domain.railway.app/api/docs`
3. Test kết nối giữa frontend và backend

## 💡 Tips

- Vercel có free tier rất tốt cho Next.js
- Hỗ trợ preview deployments cho mỗi PR
- Tự động optimize và CDN
- Analytics và monitoring tích hợp

## 🔗 Liên kết

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel Docs: https://vercel.com/docs
- Next.js on Vercel: https://vercel.com/docs/frameworks/nextjs

