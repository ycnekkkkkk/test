# Hướng dẫn Deploy cả Backend và Frontend lên Fly.io

## 📋 Yêu cầu
- Tài khoản Fly.io: https://fly.io (Free tier có sẵn)
- Fly CLI đã cài đặt
- GitHub repository đã push code

## 🚀 Cài đặt Fly CLI

### Windows (PowerShell)
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Mac/Linux
```bash
curl -L https://fly.io/install.sh | sh
```

## 🔐 Đăng nhập Fly.io

```bash
fly auth login
```

## 📦 Deploy Backend (FastAPI)

### Bước 1: Tạo App cho Backend
```bash
cd backend
fly launch --name ielts-backend --region sin
```

Khi được hỏi:
- **App name**: `ielts-backend` (hoặc để trống để tự generate)
- **Region**: `sin` (Singapore) hoặc chọn region gần bạn
- **PostgreSQL**: No (không cần, dùng SQLite)
- **Redis**: No

### Bước 2: Cấu hình Environment Variables
```bash
fly secrets set GEMINI_API_KEY=your_gemini_api_key_here
fly secrets set GEMINI_API_KEY_BACKUP=your_backup_gemini_api_key_here
fly secrets set FRONTEND_URL=https://ielts-frontend.fly.dev
fly secrets set DATABASE_URL=sqlite:///./test_session.db
```

### Bước 3: Deploy Backend
```bash
fly deploy
```

### Bước 4: Lấy URL Backend
Sau khi deploy xong, bạn sẽ có URL: `https://ielts-backend.fly.dev`

## 🎨 Deploy Frontend (Next.js)

### Bước 1: Tạo App cho Frontend
```bash
cd ../frontend
fly launch --name ielts-frontend --region sin
```

Khi được hỏi:
- **App name**: `ielts-frontend` (hoặc để trống)
- **Region**: `sin` (cùng region với backend)
- **PostgreSQL**: No
- **Redis**: No

### Bước 2: Cấu hình Environment Variables
```bash
fly secrets set NEXT_PUBLIC_API_URL=https://ielts-backend.fly.dev
fly secrets set NODE_ENV=production
```

### Bước 3: Deploy Frontend
```bash
fly deploy
```

### Bước 4: Lấy URL Frontend
Sau khi deploy xong, bạn sẽ có URL: `https://ielts-frontend.fly.dev`

## 🔄 Cập nhật CORS trong Backend

Sau khi có frontend URL, cập nhật CORS:

```bash
cd ../backend
fly secrets set FRONTEND_URL=https://ielts-frontend.fly.dev
fly deploy
```

## 📝 Kiểm tra

1. **Backend API**: `https://ielts-backend.fly.dev/api/docs` (Swagger UI)
2. **Health Check**: `https://ielts-backend.fly.dev/health`
3. **Frontend**: `https://ielts-frontend.fly.dev`

## 💰 Fly.io Free Tier

- **3 shared VMs** (đủ cho 2 apps: backend + frontend)
- **3GB persistent volume** (nếu cần database)
- **160GB outbound data transfer**
- **Không giới hạn inbound**
- **Auto-scaling**: Tự động scale down khi không dùng

## 🔧 Quản lý Apps

### Xem danh sách apps
```bash
fly apps list
```

### Xem logs
```bash
fly logs -a ielts-backend
fly logs -a ielts-frontend
```

### Scale app
```bash
fly scale count 1 -a ielts-backend
```

### Restart app
```bash
fly apps restart ielts-backend
```

## 🔄 Auto Deploy với GitHub Actions (Tùy chọn)

Tạo file `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only -a ielts-backend
        working-directory: ./backend
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only -a ielts-frontend
        working-directory: ./frontend
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

## 💡 Tips

- Fly.io tự động scale down khi không có traffic (tiết kiệm resources)
- Có thể dùng custom domain miễn phí
- Monitoring và logs tích hợp
- Dễ scale khi cần

## 🔗 Liên kết

- Fly.io Dashboard: https://fly.io/dashboard
- Fly.io Docs: https://fly.io/docs
- Fly.io Pricing: https://fly.io/docs/about/pricing/

