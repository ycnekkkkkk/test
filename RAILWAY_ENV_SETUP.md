# Cấu hình Environment Variables cho Railway

## 🔧 Backend Service (natural-adaptation-production.up.railway.app)

Vào Railway Dashboard → Backend Service → Variables, thêm:

```
DATABASE_URL=sqlite:///./test_session.db
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY_BACKUP=your_backup_gemini_api_key_here
FRONTEND_URL=https://test-production-73f1.up.railway.app
PORT=8000
```

**Lưu ý:**
- Thay `your_gemini_api_key_here` bằng API key thực tế của bạn
- `FRONTEND_URL` đã được set sẵn trong code, nhưng có thể override bằng biến này

## 🎨 Frontend Service (test-production-73f1.up.railway.app)

Vào Railway Dashboard → Frontend Service → Variables, thêm:

```
NEXT_PUBLIC_API_URL=https://natural-adaptation-production.up.railway.app
PORT=3000
NODE_ENV=production
```

**Quan trọng:** 
- `NEXT_PUBLIC_API_URL` phải trỏ đến backend URL (có `https://`)
- Sau khi set, cần **redeploy** frontend để áp dụng thay đổi

## ✅ Kiểm tra

1. **Backend API**: https://natural-adaptation-production.up.railway.app/api/docs
2. **Backend Health**: https://natural-adaptation-production.up.railway.app/health
3. **Frontend**: https://test-production-73f1.up.railway.app

## 🔄 Sau khi set Environment Variables

1. **Backend**: Tự động redeploy (hoặc manual redeploy)
2. **Frontend**: Cần **redeploy** để build lại với `NEXT_PUBLIC_API_URL` mới
   - Vào Frontend Service → Deployments → Click "Redeploy"

## 🐛 Troubleshooting

### Frontend không kết nối được backend
- Kiểm tra `NEXT_PUBLIC_API_URL` có đúng không
- Đảm bảo có `https://` prefix
- Redeploy frontend sau khi thay đổi

### CORS Error
- Backend đã được cấu hình để cho phép frontend domain
- Nếu vẫn lỗi, kiểm tra backend logs

### API không hoạt động
- Kiểm tra backend logs trong Railway Dashboard
- Kiểm tra `GEMINI_API_KEY` có đúng không
- Test API trực tiếp: https://natural-adaptation-production.up.railway.app/health

