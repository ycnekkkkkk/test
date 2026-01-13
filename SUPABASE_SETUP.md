# Hướng dẫn Setup Supabase cho Railway Backend

## 📋 Bước 1: Tạo Supabase Project

1. Đăng ký/Đăng nhập: https://supabase.com
2. Click "New Project"
3. Điền thông tin:
   - **Name**: `ielts-test` (hoặc tên bạn muốn)
   - **Database Password**: Tạo password mạnh (lưu lại!)
   - **Region**: Chọn region gần bạn (ví dụ: Southeast Asia)
4. Click "Create new project"
5. Đợi project được tạo (2-3 phút)

## 🔗 Bước 2: Lấy Connection String

1. Vào Supabase Dashboard → Project Settings → Database
2. Scroll xuống phần "Connection string"
3. Chọn tab "URI"
4. Copy connection string (dạng: `postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres`)

**Lưu ý:** Thay `[YOUR-PASSWORD]` bằng password bạn đã tạo ở bước 1

## 🔧 Bước 3: Set trong Railway

1. Vào Railway Dashboard → Backend Service → Variables
2. Thêm/Update biến:
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxx.supabase.co:5432/postgres
   ```
   (Thay `YOUR_PASSWORD` và `db.xxx.supabase.co` bằng giá trị thực tế)

3. **Hoặc dùng Connection Pooling (Khuyến nghị):**
   - Trong Supabase Dashboard → Settings → Database
   - Tìm "Connection Pooling"
   - Copy connection string từ "Connection string" (tab "Session mode" hoặc "Transaction mode")
   - Format: `postgresql://postgres.xxx:[PASSWORD]@aws-0-xxx.pooler.supabase.com:6543/postgres`
   - Pooling tốt hơn cho serverless/server applications

## 📊 Bước 4: Tạo Database Tables

Supabase sẽ tự động tạo tables khi backend start lần đầu (nhờ `Base.metadata.create_all()` trong code).

Hoặc có thể chạy SQL trực tiếp trong Supabase SQL Editor:

```sql
-- Tables sẽ được tạo tự động bởi SQLAlchemy
-- Nhưng bạn có thể kiểm tra trong Supabase Dashboard → Table Editor
```

## ✅ Bước 5: Kiểm tra

1. **Backend logs**: Kiểm tra không còn lỗi database
2. **Supabase Dashboard**: Vào Table Editor, sẽ thấy table `test_sessions`
3. **Test API**: Tạo session mới và kiểm tra trong Supabase

## 🔐 Bước 6: Bảo mật Connection String

### Option 1: Dùng Supabase Connection Pooling (Khuyến nghị)
- Tốt hơn cho production
- Hỗ trợ nhiều connections
- Format: `postgresql://postgres.xxx:[PASSWORD]@aws-0-xxx.pooler.supabase.com:6543/postgres`

### Option 2: Direct Connection
- Đơn giản hơn
- Format: `postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres`

## 💡 Tips

- **Free Tier**: Supabase free tier có 500MB database, đủ cho development
- **Connection Pooling**: Nên dùng connection pooling cho production
- **Backup**: Supabase tự động backup database
- **Monitoring**: Xem database usage trong Supabase Dashboard

## 🔗 Liên kết

- Supabase Dashboard: https://supabase.com/dashboard
- Supabase Docs: https://supabase.com/docs
- Connection Pooling: https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler

