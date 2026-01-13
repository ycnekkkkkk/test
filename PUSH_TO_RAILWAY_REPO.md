# Hướng dẫn Push Code lên GitHub Repository cho Railway

## 📋 Bước 1: Tạo Repository trên GitHub

1. Đăng nhập GitHub: https://github.com
2. Click "New" (hoặc "+" → "New repository")
3. Đặt tên: `IeltsAI`
4. Chọn **Public** hoặc **Private**
5. **KHÔNG** tích "Initialize with README" (vì đã có code)
6. Click "Create repository"

## 🚀 Bước 2: Push Code lên Repository

Sau khi tạo repository, chạy các lệnh sau:

### Windows PowerShell:
```powershell
# Thêm remote mới
git remote add railway https://github.com/neheeeee/IeltsAI.git

# Push code lên
git push railway main
```

### Nếu repository là Private và cần authentication:
```powershell
# Sử dụng Personal Access Token
git remote add railway https://YOUR_TOKEN@github.com/neheeeee/IeltsAI.git

# Hoặc sử dụng SSH (nếu đã setup SSH key)
git remote add railway git@github.com:neheeeee/IeltsAI.git
```

## 🔐 Tạo Personal Access Token (Nếu cần)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Chọn scopes: `repo` (full control)
4. Copy token
5. Sử dụng token thay cho password khi push

## ✅ Kiểm tra

Sau khi push thành công:
1. Vào https://github.com/neheeeee/IeltsAI
2. Kiểm tra code đã được push lên chưa

## 🚂 Deploy lên Railway

Sau khi code đã trên GitHub:
1. Vào Railway: https://railway.app
2. New Project → Deploy from GitHub repo
3. Chọn repository: `neheeeee/IeltsAI`
4. Deploy Backend và Frontend như hướng dẫn trong `RAILWAY_DEPLOY.md`

