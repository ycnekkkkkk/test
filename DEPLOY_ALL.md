# Hướng dẫn Deploy Cả Backend và Frontend

## 🎯 Tổng quan

Bạn có 2 lựa chọn chính để deploy cả backend và frontend:

### Option 1: Fly.io (Khuyến nghị) ⭐
- ✅ Free tier tốt (3 VMs)
- ✅ Hỗ trợ cả Python và Node.js
- ✅ Không cần refactor code
- ✅ Auto-scaling
- 📖 Xem: `FLY_DEPLOY.md`

### Option 2: Vercel (Frontend) + Vercel Serverless Functions (Backend)
- ✅ Vercel free tier tốt
- ❌ Cần refactor FastAPI sang Serverless Functions
- 📖 Xem: `VERCEL_DEPLOY.md`

## 🚀 Hướng dẫn nhanh: Fly.io

### 1. Cài đặt Fly CLI
```bash
# Windows PowerShell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### 2. Đăng nhập
```bash
fly auth login
```

### 3. Deploy Backend
```bash
cd backend
fly launch --name ielts-backend --region sin
fly secrets set GEMINI_API_KEY=your_key
fly secrets set FRONTEND_URL=https://ielts-frontend.fly.dev
fly deploy
```

### 4. Deploy Frontend
```bash
cd ../frontend
fly launch --name ielts-frontend --region sin
fly secrets set NEXT_PUBLIC_API_URL=https://ielts-backend.fly.dev
fly deploy
```

### 5. Kiểm tra
- Backend: `https://ielts-backend.fly.dev/api/docs`
- Frontend: `https://ielts-frontend.fly.dev`

## 📚 Chi tiết

Xem file hướng dẫn chi tiết:
- `FLY_DEPLOY.md` - Deploy lên Fly.io (Backend + Frontend)
- `VERCEL_DEPLOY.md` - Deploy Frontend lên Vercel
- `RENDER_DEPLOY.md` - Deploy Backend lên Render (nếu cần)

