# 🎬 KỊCH BẢN DEMO FULL HỆ THỐNG POS
## Dành cho người chưa biết gì về hệ thống

---

## 📋 BẢNG TÀI KHOẢN ĐẦY ĐỦ (Đã tạo sẵn)

| # | Role | Email | Password | Dashboard | Nhiệm vụ |
|---|------|-------|----------|-----------|---------|
| 1 | **Super Admin** | `admin@pos.com` | `Admin@123` | `/super-admin` | Quản lý toàn hệ thống |
| 2 | **Store Admin** | `demo@pospro.com` | `demo123` | `/store` | Chủ cửa hàng |
| 3 | **Store Manager** | `storemanager@pos.com` | `Demo@123` | `/store` | Quản lý cửa hàng |
| 4 | **Branch Admin** | `branchadmin@pos.com` | `Demo@123` | `/branch` | Quản lý chi nhánh |
| 5 | **Branch Manager** | `branchmanager@pos.com` | `Demo@123` | `/branch` | Nhân viên quản lý |
| 6 | **Cashier (Thu ngân)** | `cashier@pos.com` | `Demo@123` | `/cashier` | Bán hàng POS |

> **Cấu trúc hiện tại:**
> Store: **"Demo Store"** (ID=3) → Branch: **"Downtown Branch"** (ID=1)

---

## 🗺️ SƠ ĐỒ PHÂN CẤP

```
SUPER ADMIN (admin@pos.com)
    │  Quản lý toàn hệ thống, tạo Store Admin
    │
    ▼
STORE ADMIN (demo@pospro.com)  ←── Chủ "Demo Store"
    │  Quản lý cửa hàng: sản phẩm, nhân viên, chi nhánh
    │
    ├── STORE MANAGER (storemanager@pos.com)
    │       Hỗ trợ quản lý store
    │
    └── DOWNTOWN BRANCH (Chi nhánh 1)
            │
            ├── BRANCH ADMIN (branchadmin@pos.com)
            │       Quản lý chi nhánh
            │
            ├── BRANCH MANAGER (branchmanager@pos.com)
            │       Xem báo cáo chi nhánh
            │
            └── CASHIER (cashier@pos.com)
                    Bán hàng tại quầy POS
```

---

## 🎯 KỊCH BẢN DEMO — TỪNG BƯỚC

### ═══ GIAI ĐOẠN 1: SUPER ADMIN ═══
**Thời gian:** ~2 phút | **Tài khoản:** `admin@pos.com` / `Admin@123`

**Bước 1.1** — Đăng nhập Super Admin
- Vào: http://localhost:5173/auth/login
- Điền email + password → Sign In
- ✅ Redirect tự động → `/super-admin`

**Bước 1.2** — Xem tổng quan hệ thống
- Dashboard hiện: Tổng số stores, doanh thu, users
- Menu trái: **Stores | Subscriptions | Users**

**Bước 1.3** — Xem danh sách Stores đã đăng ký
- Click **Stores** → Thấy "Demo Store" đã tạo
- Đây là nơi Super Admin kiểm soát toàn bộ cửa hàng trong hệ thống

**Bước 1.4** — Xem Subscription Plans
- Click **Subscriptions** → Xem các gói: Basic, Pro, Enterprise
- Super Admin tạo/sửa gói subscription cho Store Admin mua

**📌 Kết thúc giai đoạn 1 → Logout**

---

### ═══ GIAI ĐOẠN 2: STORE ADMIN — QUẢN LÝ CỬA HÀNG ═══
**Thời gian:** ~5 phút | **Tài khoản:** `demo@pospro.com` / `demo123`

**Bước 2.1** — Đăng nhập Store Admin
- Login → Redirect → `/store`
- Dashboard hiện: Doanh thu, đơn hàng, sản phẩm tổng quan của "Demo Store"

**Bước 2.2** — Tạo Category (Danh mục sản phẩm)
- Menu trái → **Categories** (hoặc Products → Categories)
- Nhấn **Add Category**
- Nhập: Tên = "Đồ uống", mô tả tùy ý
- Nhấn **Save** → ✅ Category xuất hiện trong danh sách

> 💡 **Dữ liệu chạy ngầm:**
> FE gọi: `POST http://localhost:8080/api/categories`
> Body: `{"name":"Đồ uống","storeId":3}`
> DB: INSERT vào bảng `categories`

**Bước 2.3** — Tạo Product (Sản phẩm)
- Menu → **Products** → **Add Product**
- Điền:
  - Name: `Cà phê đen`
  - SKU: `CF001`
  - Price: `25000`
  - Category: chọn "Đồ uống" (vừa tạo)
  - Quantity: `100`
  - Description: `Cà phê đen truyền thống`
- Nhấn **Save** → ✅ Sản phẩm xuất hiện

> 💡 **Dữ liệu chạy ngầm:**
> FE gọi: `POST http://localhost:8080/api/products`
> DB: INSERT vào bảng `products` với `store_id=3`

**Bước 2.4** — Xem/Sửa Product
- Click vào sản phẩm → Edit → Sửa giá thành `28000` → Update
- FE gọi: `PATCH http://localhost:8080/api/products/{id}`
- DB: UPDATE bảng `products`

**Bước 2.5** — Quản lý Branch (Chi nhánh)
- Menu → **Branches** → Thấy "Downtown Branch"
- Có thể tạo thêm branch mới, xem thông tin chi nhánh

**Bước 2.6** — Quản lý Employees (Nhân viên)
- Menu → **Employees** → Xem danh sách nhân viên của store
- Thấy: Store Manager, Branch Admin, Branch Manager, Cashier đã tạo

**📌 Kết thúc giai đoạn 2 → Logout**

---

### ═══ GIAI ĐOẠN 3: BRANCH ADMIN — QUẢN LÝ CHI NHÁNH ═══
**Thời gian:** ~2 phút | **Tài khoản:** `branchadmin@pos.com` / `Demo@123`

**Bước 3.1** — Đăng nhập Branch Admin
- Login → Redirect → `/branch`
- Dashboard của "Downtown Branch"

**Bước 3.2** — Xem Inventory (Tồn kho)
- Menu → **Inventory** → Xem sản phẩm trong kho chi nhánh
- Tồn kho được quản lý theo từng branch

**Bước 3.3** — Xem Orders (Đơn hàng) của chi nhánh
- Menu → **Orders** → Danh sách đơn hàng tại Downtown Branch
- (Ban đầu trống — sẽ có sau khi Cashier bán hàng)

**Bước 3.4** — Xem báo cáo Branch Analytics
- Menu → **Analytics** → Biểu đồ doanh thu, sản phẩm bán chạy của chi nhánh

**📌 Kết thúc giai đoạn 3 → Logout**

---

### ═══ GIAI ĐOẠN 4: CASHIER — BÁN HÀNG TẠI QUẦY ═══
**Thời gian:** ~3 phút | **Tài khoản:** `cashier@pos.com` / `Demo@123`

**Bước 4.1** — Đăng nhập Cashier
- Login → Redirect → `/cashier`
- Màn hình POS: danh sách sản phẩm bên trái, giỏ hàng bên phải

**Bước 4.2** — Tìm và chọn sản phẩm
- Tìm kiếm "Cà phê đen" (sản phẩm vừa tạo ở Bước 2.3)
- Click vào sản phẩm → Thêm vào giỏ hàng

**Bước 4.3** — Điều chỉnh giỏ hàng
- Tăng/giảm số lượng
- Xem tổng tiền tự động tính

**Bước 4.4** — Thanh toán tiền mặt
- Chọn phương thức: **Cash**
- Nhập số tiền khách đưa → Hệ thống tính tiền thừa
- Nhấn **Complete Payment** / **Place Order**
- ✅ Đơn hàng được tạo

> 💡 **Dữ liệu chạy ngầm:**
> FE gọi: `POST http://localhost:8080/api/orders`
> Body: `{"items":[{"productId":1,"quantity":2}],"paymentMethod":"CASH","branchId":1}`
> DB: INSERT vào bảng `orders` + `order_items`

**Bước 4.5** — In/Xem hóa đơn
- Sau thanh toán → Hiện receipt/hóa đơn
- Có thể in hoặc reset để bán đơn tiếp theo

**📌 Kết thúc giai đoạn 4 → Logout**

---

### ═══ GIAI ĐOẠN 5: QUAY LẠI STORE ADMIN — XEM KẾT QUẢ ═══
**Thời gian:** ~2 phút | **Tài khoản:** `demo@pospro.com` / `demo123`

**Bước 5.1** — Login lại Store Admin
- Vào `/store` → Dashboard hiện doanh thu mới nhất

**Bước 5.2** — Xem Analytics
- Menu → **Analytics**
- Biểu đồ doanh thu theo ngày/tuần/tháng
- Sản phẩm bán chạy nhất
- Doanh thu theo chi nhánh

**Bước 5.3** — Xem Orders
- Menu → **Orders** → Thấy đơn hàng Cashier vừa tạo
- Chi tiết đơn: sản phẩm, số lượng, tổng tiền, thời gian

**Bước 5.4** — Xem Inventory
- Menu → **Inventory** → Tồn kho đã giảm sau khi bán

---

## 🔍 CÁCH XEM DỮ LIỆU RA VÀO FE ↔ BE (Dùng DevTools)

### Mở DevTools:
- Nhấn **F12** trên Windows / **Cmd+Option+I** trên Mac
- Chọn tab **Network**
- Tick ✅ **XHR** hoặc **Fetch** để lọc chỉ API calls

### Đọc 1 request:
```
Khi bạn click "Add Product":

▶ Request (FE → BE):
  Method:  POST
  URL:     http://localhost:8080/api/products
  Headers: Authorization: Bearer eyJhbGci...  ← JWT Token
  Body:    {"name":"Cà phê","price":25000,"storeId":3}

◀ Response (BE → FE):
  Status:  200 OK
  Body:    {"id":1,"name":"Cà phê","price":25000,...}
           ↑ Dữ liệu đã lưu vào DB, trả về cho FE hiện lên màn hình
```

### Xem token JWT:
- Mở DevTools → Tab **Application** → **Local Storage** → `localhost:5173`
- Thấy key `jwt` hoặc `token` → Đây là token xác thực gửi kèm mỗi request

---

## 🗄️ XEM DỮ LIỆU TRONG DATABASE

Mở Terminal, chạy:
```bash
/Applications/XAMPP/xamppfiles/bin/mysql -u root pos
```

Các lệnh hữu ích:
```sql
-- Xem đơn hàng mới nhất
SELECT * FROM orders ORDER BY created_at DESC LIMIT 5;

-- Xem sản phẩm
SELECT id, name, price, store_id FROM products;

-- Xem categories
SELECT * FROM categories;

-- Xem inventory (tồn kho)
SELECT * FROM inventories;

-- Kiểm tra sau khi bán hàng
SELECT o.id, o.total_price, o.payment_method, o.created_at
FROM orders o ORDER BY o.created_at DESC;
```

---

## ⚡ CHECKLIST DEMO NHANH (Copy & paste để không quên)

```
[ ] 1. Mở XAMPP → Start All (MySQL phải "Running")
[ ] 2. Terminal 1: cd pos-backend && ./mvnw spring-boot:run
[ ] 3. Terminal 2: export PATH="/opt/homebrew/opt/node@20/bin:$PATH"
                   cd pos-frontend-vite && pnpm dev
[ ] 4. Chờ thấy "Started PosSystemApplication" + "VITE ready"
[ ] 5. Mở http://localhost:5173

GIAI ĐOẠN 1 - SUPER ADMIN:
[ ] Login: admin@pos.com / Admin@123
[ ] Xem Stores list, Subscription plans
[ ] Logout

GIAI ĐOẠN 2 - STORE ADMIN:
[ ] Login: demo@pospro.com / demo123
[ ] Tạo Category "Đồ uống"
[ ] Tạo Product "Cà phê đen" giá 25000
[ ] Xem Branches, Employees
[ ] Logout

GIAI ĐOẠN 3 - CASHIER:
[ ] Login: cashier@pos.com / Demo@123
[ ] Chọn "Cà phê đen" → Thêm vào giỏ
[ ] Thanh toán Cash → Complete
[ ] Xem hóa đơn
[ ] Logout

GIAI ĐOẠN 4 - STORE ADMIN (kiểm tra kết quả):
[ ] Login: demo@pospro.com / demo123
[ ] Xem Analytics → biểu đồ doanh thu
[ ] Xem Orders → đơn vừa tạo
[ ] Xem Inventory → tồn kho giảm
```

---

*URL Frontend: http://localhost:5173 | Backend: http://localhost:8080*
*Store: Demo Store (ID=3) | Branch: Downtown Branch (ID=1)*
