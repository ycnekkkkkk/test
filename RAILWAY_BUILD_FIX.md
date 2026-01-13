# Fix "Killed" Error khi Build Next.js trên Railway

## 🔴 Vấn đề
Lỗi "Killed" xảy ra khi build Next.js do hết memory (OOM - Out of Memory). Railway free tier có giới hạn memory.

## ✅ Giải pháp đã áp dụng

### 1. Tối ưu Next.js Config
- Bật `swcMinify` để dùng SWC minifier (nhanh hơn, ít memory hơn)
- Tắt console.log trong production
- Tắt CSS optimization
- Tắt source maps trong production

### 2. Giới hạn Memory cho Node.js
- Set `NODE_OPTIONS='--max-old-space-size=1024'` (1GB)
- Áp dụng cho cả build command

### 3. Tách Build và Start Command
- Build command: Chạy trong build phase
- Start command: Chỉ chạy `npm start` (không build lại)

## 🔧 Cấu hình trong Railway Dashboard

### Frontend Service Settings

**Tab "Source":**
- Root Directory: `frontend`
- Build Command: `NODE_OPTIONS='--max-old-space-size=1024' npm run build`
- Start Command: `npm start`

**Hoặc để Railway tự động:**
- Root Directory: `frontend`
- Build Command: (để trống - Railway sẽ dùng từ `railway.json`)
- Start Command: (để trống - Railway sẽ dùng từ `railway.json`)

## 💡 Nếu vẫn bị lỗi

### Option 1: Tăng Memory Limit
Nếu có thể, upgrade Railway plan để có nhiều memory hơn.

### Option 2: Build Locally và Deploy
1. Build locally: `cd frontend && npm run build`
2. Commit `.next` folder (tạm thời)
3. Deploy với start command: `npm start`

### Option 3: Sử dụng Build Cache
Railway tự động cache `node_modules`, nhưng có thể thêm:
- Cache `.next/cache` folder

## 📝 Kiểm tra

Sau khi deploy, kiểm tra logs:
- Build thành công không còn "Killed"
- Service start thành công

