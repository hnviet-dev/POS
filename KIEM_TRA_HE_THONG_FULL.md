# 🔍 BÁO CÁO KIỂM TRA HỆ THỐNG POS — TOÀN BỘ

> Thực hiện: 2026-05-10 | Máy: MacBook M1 | Backend: :8080 | Frontend: :5173

---

## 📊 TỔNG QUAN TRẠNG THÁI

| Module | API | Status | Ghi chú |
|--------|-----|--------|---------|
| Auth | POST /auth/login | ✅ OK | JWT hoạt động |
| Auth | POST /auth/signup | ✅ OK | Không cho tạo ROLE_ADMIN qua API (by design) |
| Super Admin | GET /api/super-admin | ✅ OK | Cần storeId param |
| Subscription Plans | GET /api/super-admin/subscription-plans | ✅ OK | |
| Stores | GET/POST /api/stores | ✅ OK | |
| Products | GET /api/products/store/{id} | ✅ OK | Cần storeId |
| Categories | GET /api/categories/store/{id} | ✅ OK | Cần storeId |
| Orders | GET /api/orders/branch/{id} | ✅ OK | Cần branchId |
| Inventory | GET /api/inventories/branch/{id} | ✅ OK | Cần branchId |
| Customers | GET /api/customers | ✅ OK | |
| Employees | GET /api/employees/store/{id} | ✅ OK | Cần storeId |
| Branches | GET /api/branches/store/{id} | ✅ OK | Cần storeId |
| Analytics | GET /api/store/analytics | ✅ OK | Cần storeId param |
| Shift Reports | GET /api/shift-reports | ✅ OK | |

> ⚠️ Các API trả 400 khi gọi không có `storeId`/`branchId` là **đúng thiết kế** — không phải lỗi.

---

## 🔄 LUỒNG DỮ LIỆU — HƯỚNG DẪN TEST TỪNG BƯỚC

### LUỒNG 1: Super Admin → Tạo Store Admin

**Bước 1.1** — Đăng nhập Super Admin
- URL: http://localhost:5173/auth/login
- Email: `admin@pos.com` | Password: `Admin@123`
- Kết quả: Redirect → `/super-admin`

**Bước 1.2** — Tạo Store Admin
- Vào `/super-admin` → Tìm "Create Store Admin" hoặc "Add User"
- Điền thông tin Store Admin mới
- DB thay đổi: Bảng `users` thêm 1 row với `role = 1` (ROLE_STORE_ADMIN)

**Kiểm tra DB:**
```sql
SELECT id, email, role FROM users;
-- role=0: ADMIN | role=1: STORE_ADMIN | role=2: STORE_MANAGER
-- role=3: BRANCH_MANAGER | role=4: BRANCH_ADMIN | role=5: CASHIER
```

---

### LUỒNG 2: Store Admin → Onboarding → Tạo Store

**Bước 2.1** — Đăng nhập Store Admin
- Email: `demo@pospro.com` | Password: `demo123`
- Kết quả: Redirect → `/store` hoặc màn hình Onboarding

**Bước 2.2** — Tạo Store (Onboarding)
- Điền thông tin cửa hàng: tên, địa chỉ, điện thoại
- API gọi: `POST /api/stores`
- DB thay đổi: Bảng `stores` thêm 1 row, `users.store_id` được cập nhật

**Kiểm tra DB:**
```sql
SELECT id, name, email FROM stores;
SELECT id, email, store_id FROM users;
```

---

### LUỒNG 3: Store Admin → Tạo Category + Product

**Bước 3.1** — Tạo Category
- URL: http://localhost:5173/store/categories
- Nhấn "Add Category" → Nhập tên
- API: `POST /api/categories`
- DB: Bảng `categories` thêm row

**Bước 3.2** — Tạo Product
- URL: http://localhost:5173/store/products
- Nhấn "Add Product" → Điền tên, giá, category, upload ảnh (Cloudinary)
- API: `POST /api/products`
- DB: Bảng `products` thêm row

**Kiểm tra DB:**
```sql
SELECT id, name FROM categories;
SELECT id, name, price, store_id FROM products;
```

---

### LUỒNG 4: Store Admin → Tạo Branch + Nhân viên

**Bước 4.1** — Tạo Branch
- URL: http://localhost:5173/store/branches
- API: `POST /api/branches`
- DB: Bảng `branches` thêm row

**Bước 4.2** — Thêm nhân viên vào Branch
- API: `POST /api/employees/branch/{branchId}`
- DB: Bảng `users` thêm row với `branch_id`

**Kiểm tra DB:**
```sql
SELECT id, name, store_id FROM branches;
SELECT id, email, role, branch_id FROM users WHERE branch_id IS NOT NULL;
```

---

### LUỒNG 5: Cashier → Bán hàng (POS chính)

**Bước 5.1** — Đăng nhập Cashier
- Dùng tài khoản ROLE_BRANCH_CASHIER
- Redirect → `/cashier`

**Bước 5.2** — Tạo đơn hàng
- Chọn sản phẩm → Thêm vào giỏ → Chọn thanh toán tiền mặt → Xác nhận
- API: `POST /api/orders`
- DB: Bảng `orders` + `order_items` thêm rows

**Bước 5.3** — Kiểm tra đơn hàng
```sql
SELECT id, total_price, status, created_at FROM orders ORDER BY created_at DESC LIMIT 5;
```

---

### LUỒNG 6: Store Admin → Xem Analytics

- URL: http://localhost:5173/store/analytics
- API: `GET /api/store/analytics?storeId=X&...`
- Hiện biểu đồ doanh thu, sản phẩm bán chạy

---

## 🧪 LỆNH KIỂM TRA DATABASE NHANH

Mở Terminal và chạy:

```bash
/Applications/XAMPP/xamppfiles/bin/mysql -u root pos
```

Trong MySQL shell:

```sql
-- Xem tất cả bảng
SHOW TABLES;

-- Kiểm tra users
SELECT id, email, full_name, role, store_id, branch_id FROM users;

-- Kiểm tra stores
SELECT id, name, email FROM stores;

-- Kiểm tra products
SELECT id, name, price, store_id FROM products LIMIT 10;

-- Kiểm tra orders
SELECT id, total_price, status, branch_id, created_at FROM orders ORDER BY created_at DESC LIMIT 5;

-- Kiểm tra categories
SELECT id, name, store_id FROM categories;
```

---

## ❓ CÂU HỎI THƯỜNG GẶP KHI DEMO

**Q: Vào /store bị Page Not Found?**
→ Chưa đăng nhập. Phải đăng nhập ở `/auth/login` trước, hệ thống tự redirect.

**Q: XAMPP "Index of /" là gì?**
→ Đây là Apache của XAMPP (port 80), không liên quan POS. POS chỉ dùng MySQL (port 3306).

**Q: Backend port 5000 hay 8080?**
→ **8080** — vì macOS chiếm port 5000 (AirPlay Receiver). Đã cấu hình lại.

**Q: Cloudinary ảnh có hoạt động không?**
→ ✅ Có — đã cấu hình sẵn trong code, không cần làm gì thêm.

**Q: Stripe/Email có cần không?**
→ ❌ Không cần cho demo cơ bản. Chỉ cần nếu demo thanh toán online hoặc quên mật khẩu.

---

## 🎬 KỊCH BẢN DEMO NGẮN (5 phút)

1. **Mở** http://localhost:5173 → Giới thiệu Landing Page
2. **Login** admin@pos.com / Admin@123 → Super Admin Dashboard
3. **Login** demo@pospro.com / demo123 → Store Dashboard  
4. Tạo **Category** → Tạo **Product** (upload ảnh Cloudinary)
5. Vào **Cashier** → Chọn sản phẩm → Thanh toán tiền mặt
6. Quay lại **Store** → Xem **Analytics** → Biểu đồ doanh thu
