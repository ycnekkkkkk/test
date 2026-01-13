# Fix PostgreSQL Connection Error trên Railway

## 🔴 Vấn đề
```
ModuleNotFoundError: No module named 'psycopg2'
```

Lỗi này xảy ra khi:
- Railway tự động tạo PostgreSQL database và set `DATABASE_URL`
- Hoặc bạn đã thêm PostgreSQL service trong Railway
- Nhưng thiếu `psycopg2` trong requirements.txt

## ✅ Đã sửa

1. **Thêm `psycopg2-binary` vào requirements.txt**
   - Module cần thiết để kết nối PostgreSQL
   - `psycopg2-binary` dễ cài đặt hơn `psycopg2` (không cần compile)

2. **Cải thiện database connection handling**
   - Tự động fallback về SQLite nếu PostgreSQL fail
   - Better error handling

## 🔧 Cấu hình trong Railway

### Option 1: Dùng SQLite (Đơn giản - cho development)

Trong Backend Service → Variables:
```
DATABASE_URL=sqlite:///./test_session.db
```

**Lưu ý:** SQLite sẽ bị reset mỗi lần redeploy trên Railway.

### Option 2: Dùng PostgreSQL (Khuyến nghị - cho production)

1. **Thêm PostgreSQL Service:**
   - Railway Dashboard → Project → New → Database → Add PostgreSQL
   - Railway tự động tạo và set `DATABASE_URL` environment variable

2. **Kiểm tra DATABASE_URL:**
   - Vào Backend Service → Variables
   - Sẽ thấy `DATABASE_URL` tự động được set (dạng: `postgresql://...`)

3. **Không cần set thủ công** - Railway tự động set rồi

## 📝 Sau khi thêm PostgreSQL

1. Railway sẽ tự động redeploy backend
2. Backend sẽ tự động tạo tables khi start
3. Database sẽ persist qua các lần redeploy

## 🐛 Troubleshooting

### Nếu vẫn lỗi "No module named 'psycopg2'"
- Kiểm tra requirements.txt đã có `psycopg2-binary` chưa
- Redeploy backend để cài lại dependencies

### Nếu muốn dùng SQLite thay vì PostgreSQL
- Xóa PostgreSQL service (nếu đã thêm)
- Set `DATABASE_URL=sqlite:///./test_session.db` trong Variables
- Redeploy backend

## 💡 Lưu ý

- **SQLite**: Đơn giản nhưng mất data khi redeploy
- **PostgreSQL**: Phức tạp hơn nhưng data persist, tốt cho production

