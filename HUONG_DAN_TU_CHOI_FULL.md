# 🎓 HƯỚNG DẪN TỰ TAY DEMO HỆ THỐNG POS
## Từ đầu đến cuối — Không cần biết code

> Đây là hướng dẫn để **bạn tự thao tác** trên màn hình, hiểu từng bước,  
> biết mình đang làm gì và tại sao.

---

## 🗂️ BẢNG TÀI KHOẢN SẴN SÀNG

| Tài khoản | Email | Password | Vào trang |
|-----------|-------|----------|-----------|
| Super Admin | `admin@pos.com` | `Admin@123` | `/super-admin` |
| Store Admin | `demo@pospro.com` | `demo123` | `/store` |
| Store Manager | `storemanager@pos.com` | `Demo@123` | `/store` |
| Branch Admin | `branchadmin@pos.com` | `Demo@123` | `/branch` |
| Branch Manager | `branchmanager@pos.com` | `Demo@123` | `/branch` |
| Thu ngân (Cashier) | `cashier@pos.com` | `Demo@123` | `/cashier` |

> ⚠️ **Luôn vào từ:** http://localhost:5173/auth/login  
> Không gõ thẳng `/store` hay `/cashier` khi chưa login

---

## 🔑 HIỂU CƠ CHẾ TRƯỚC KHI BẮT ĐẦU

Hệ thống POS có 3 tầng:

```
SUPER ADMIN
  → Quản lý toàn bộ hệ thống (tất cả cửa hàng)
  → Tạo gói Subscription (Basic/Pro/Enterprise)
  → Xem tất cả cửa hàng đã đăng ký

STORE ADMIN / STORE MANAGER  
  → Quản lý 1 cửa hàng cụ thể
  → Tạo sản phẩm, danh mục, chi nhánh, nhân viên

BRANCH ADMIN / MANAGER / CASHIER
  → Làm việc tại 1 chi nhánh
  → Cashier: bán hàng trực tiếp tại quầy
```

**Quan hệ dữ liệu:**
```
Super Admin tạo → Store Admin
Store Admin tạo → Store (cửa hàng) → Branch (chi nhánh)
Store Admin tạo → Products, Categories
Branch → Cashier bán hàng → Orders (đơn hàng)
```

---

## ═══════════════════════════════════
## 🔴 GIAI ĐOẠN 1 — SUPER ADMIN
## ═══════════════════════════════════

### Bạn đang đóng vai: Chủ nền tảng POS

**Mở trình duyệt → http://localhost:5173/auth/login**

### Bước 1.1 — Đăng nhập

1. Click vào ô **Email Address** → Xóa sạch → Gõ: `admin@pos.com`
2. Click vào ô **Password** → Xóa sạch → Gõ: `Admin@123`
3. Click nút **Sign In** (màu hồng)
4. ✅ Tự động chuyển sang `/super-admin`

**Bạn sẽ thấy:** Dashboard tổng quan với menu bên trái gồm:
- 📊 Dashboard
- 🏪 Stores
- 💳 Subscription Plans
- ⏳ Pending Requests
- ⚙️ Settings

---

### Bước 1.2 — Xem Subscription Plans (Gói dịch vụ)

**Click "Subscription Plans" trên menu trái**

Bạn thấy danh sách các gói: Basic, Pro, Enterprise...  
→ Đây là các gói mà **Store Admin phải mua** để dùng hệ thống

**Thử tạo 1 gói mới:**
1. Click **"Add New Plan"** (góc trên phải)
2. Form hiện ra với các trường:
   - Plan Name (Tên gói)
   - Price (Giá)
   - Features (Tính năng)
3. ❌ **Không cần submit** — chỉ xem để hiểu cấu trúc
4. Đóng form lại

---

### Bước 1.3 — Xem Stores (Cửa hàng đã đăng ký)

**Click "Stores" trên menu trái**

Bạn thấy danh sách các cửa hàng đã tạo trong hệ thống.  
→ Ở đây có "Demo Store" đã được tạo từ trước

**Để tạo Store Admin mới (luồng thật):**  
1. Click **"Add Store"** hoặc **"Create"**
2. Điền: Store Name, Email (cho Store Admin), Password, chọn Subscription Plan
3. → Hệ thống tạo tài khoản Store Admin và cửa hàng cùng lúc

> 💡 **Dữ liệu thực tế:** Khi bạn tạo Store ở đây, database sẽ INSERT 1 row vào bảng `stores` và 1 row vào bảng `users` với role=ROLE_STORE_ADMIN

---

### Bước 1.4 — Logout

Kéo xuống cuối menu trái → Click **Logout**  
✅ Về lại trang Login

---

## ═══════════════════════════════════
## 🟠 GIAI ĐOẠN 2 — STORE ADMIN
## ═══════════════════════════════════

### Bạn đang đóng vai: Chủ cửa hàng "Demo Store"

### Bước 2.1 — Đăng nhập Store Admin

1. Vào http://localhost:5173/auth/login
2. Email: `demo@pospro.com` | Password: `demo123`
3. Click Sign In
4. ✅ Vào `/store` — Dashboard của cửa hàng

**Menu bên trái bạn thấy:**
- 📊 Dashboard
- 🏪 Branches (Chi nhánh)
- 📦 Products (Sản phẩm)
- 🏷️ Categories (Danh mục)
- 👥 Employees (Nhân viên)
- 💰 Sales (Doanh thu)
- 📈 Reports
- ⚙️ Settings
- ⬆️ Upgrade Plan

---

### Bước 2.2 — Tạo Category (Danh mục sản phẩm)

> **Phải tạo Category TRƯỚC khi tạo Product**

1. Click **"Categories"** trên menu
2. Click **"Add Category"** (nút góc trên phải)
3. Form hiện ra — điền:
   - **Name:** `Đồ uống`
   - **Description:** `Các loại đồ uống`
4. Click **Save / Create**
5. ✅ Category "Đồ uống" xuất hiện trong danh sách

> 💡 **Phía sau màn hình:** Frontend gọi `POST /api/categories {"name":"Đồ uống","storeId":3}` → Backend lưu vào bảng `categories` trong MySQL

---

### Bước 2.3 — Tạo Product (Sản phẩm)

1. Click **"Products"** trên menu
2. Click **"Add Product"**
3. Điền form:
   - **Name:** `Cà phê đen`
   - **SKU:** `CF001`
   - **Category:** Chọn "Đồ uống" (vừa tạo)
   - **MRP (giá gốc):** `30000`
   - **Selling Price (giá bán):** `25000`
   - **Description:** `Cà phê đen truyền thống`
4. Click **Save**
5. ✅ Sản phẩm xuất hiện trong danh sách

> 💡 **Phía sau màn hình:** `POST /api/products` → INSERT vào bảng `products`

**Thử tạo thêm 1 sản phẩm nữa:**
- Name: `Trà sữa` | SKU: `TS001` | Price: `35000`

---

### Bước 2.4 — Xem Branches (Chi nhánh)

1. Click **"Branches"** trên menu
2. Bạn thấy chi nhánh **"Downtown Branch"** đã tồn tại
3. Click vào chi nhánh để xem chi tiết: địa chỉ, giờ mở cửa, manager

**Để tạo chi nhánh mới (demo):**
1. Click "Add Branch"
2. Điền: Tên, Địa chỉ, Điện thoại, Email, Giờ mở cửa
3. → Chi nhánh mới sẽ xuất hiện

---

### Bước 2.5 — Xem Employees (Nhân viên)

1. Click **"Employees"** trên menu
2. Xem danh sách nhân viên gắn với store này

> ⚠️ Nếu danh sách trống — đây là vấn đề hiển thị. Nhân viên đã tồn tại trong DB nhưng UI có thể cần refresh.

---

### Bước 2.6 — Logout Store Admin

Kéo xuống cuối menu trái → Click **Logout**

---

## ═══════════════════════════════════
## 🟡 GIAI ĐOẠN 3 — CASHIER (THU NGÂN)
## ═══════════════════════════════════

### Bạn đang đóng vai: Thu ngân tại Downtown Branch

### Bước 3.1 — Đăng nhập Cashier

1. Vào http://localhost:5173/auth/login
2. Email: `cashier@pos.com` | Password: `Demo@123`
3. Click Sign In
4. ✅ Vào `/cashier` — Màn hình POS bán hàng

**Màn hình POS gồm 2 phần:**
- **Bên trái:** Danh sách sản phẩm (tìm kiếm, chọn category)
- **Bên phải:** Giỏ hàng, tổng tiền, thanh toán

---

### Bước 3.2 — Thực hiện bán hàng

**a) Tìm và thêm sản phẩm:**
1. Tìm "Cà phê đen" trong danh sách
2. Click vào sản phẩm → Thêm vào giỏ hàng (bên phải)
3. Tăng số lượng nếu cần (nút + / -)

**b) Thêm sản phẩm thứ 2:**
1. Tìm "Trà sữa" → Click để thêm vào giỏ

**c) Xem giỏ hàng:**
- Bên phải hiện: Danh sách items, số lượng, đơn giá, tổng tiền
- Tổng được tính tự động

**d) Thanh toán:**
1. Chọn phương thức: **Cash** (Tiền mặt)
2. Nhập số tiền khách đưa (ví dụ: 100,000đ)
3. Hệ thống tính tiền thừa tự động
4. Click **"Complete Payment"** hoặc **"Place Order"**
5. ✅ Đơn hàng hoàn thành → Hiện hóa đơn

> 💡 **Phía sau màn hình:**
> `POST /api/orders {"items":[{"productId":X,"quantity":1}],"paymentMethod":"CASH","branchId":1}`
> → INSERT vào bảng `orders` và `order_items`

---

### Bước 3.3 — Logout Cashier

---

## ═══════════════════════════════════
## 🟢 GIAI ĐOẠN 4 — QUAY LẠI STORE ADMIN
## ═══════════════════════════════════

### Bước 4.1 — Đăng nhập lại Store Admin

Email: `demo@pospro.com` / `demo123`

### Bước 4.2 — Xem kết quả bán hàng

**Sales / Orders:**
1. Click "Sales" → Thấy đơn hàng vừa tạo
2. Click vào đơn → Xem chi tiết: sản phẩm, số lượng, tổng tiền, thời gian, cashier

**Analytics/Reports:**
1. Click "Reports" hoặc "Analytics"  
2. Biểu đồ doanh thu theo ngày
3. Sản phẩm bán chạy nhất
4. So sánh các chi nhánh

---

## 🔍 CÁCH XEM DỮ LIỆU THỰC TẾ TRONG DATABASE

**Mở Terminal, gõ:**
```bash
/Applications/XAMPP/xamppfiles/bin/mysql -u root pos
```

**Các lệnh SQL hữu ích:**
```sql
-- Xem tất cả sản phẩm
SELECT id, name, price FROM products;

-- Xem đơn hàng mới nhất
SELECT id, total_price, payment_method, created_at 
FROM orders ORDER BY created_at DESC LIMIT 5;

-- Xem items trong đơn hàng
SELECT oi.quantity, p.name, oi.price
FROM order_items oi JOIN products p ON oi.product_id = p.id
WHERE oi.order_id = 1;

-- Xem tất cả users và role của họ
SELECT email, full_name, 
  CASE role 
    WHEN 0 THEN 'SUPER_ADMIN'
    WHEN 1 THEN 'STORE_ADMIN'
    WHEN 2 THEN 'STORE_MANAGER'
    WHEN 3 THEN 'BRANCH_MANAGER'
    WHEN 4 THEN 'BRANCH_ADMIN'
    WHEN 5 THEN 'CASHIER'
  END as role_name
FROM users;
```

---

## 🔍 XEM API REQUEST BẰNG DEVTOOLS

1. Nhấn **F12** (hoặc Cmd+Option+I trên Mac)
2. Chọn tab **Network**
3. Click **XHR** để lọc API calls
4. Thực hiện action bất kỳ (ví dụ: thêm sản phẩm)
5. Thấy request xuất hiện → Click vào → Xem:
   - **Headers**: URL gọi đến đâu, có JWT token không
   - **Payload**: Dữ liệu gửi đi
   - **Response**: Dữ liệu backend trả về

---

## ✅ CHECKLIST TỰ TEST NHANH

```
GIAI ĐOẠN 1 — SUPER ADMIN (admin@pos.com / Admin@123)
[ ] Vào /super-admin
[ ] Xem Subscription Plans hiện có
[ ] Xem Stores list
[ ] Logout

GIAI ĐOẠN 2 — STORE ADMIN (demo@pospro.com / demo123)
[ ] Vào /store
[ ] Tạo Category "Đồ uống"
[ ] Tạo Product "Cà phê đen" giá 25,000
[ ] Tạo Product "Trà sữa" giá 35,000
[ ] Xem Branches → "Downtown Branch"
[ ] Logout

GIAI ĐOẠN 3 — CASHIER (cashier@pos.com / Demo@123)
[ ] Vào /cashier
[ ] Thêm "Cà phê đen" vào giỏ
[ ] Thêm "Trà sữa" vào giỏ
[ ] Chọn Cash → Nhập tiền → Complete Payment
[ ] Xem hóa đơn
[ ] Logout

GIAI ĐOẠN 4 — STORE ADMIN kiểm tra
[ ] Login lại demo@pospro.com
[ ] Xem Sales/Orders → thấy đơn vừa bán
[ ] Xem Analytics → biểu đồ doanh thu
[ ] Mở Terminal → mysql → SELECT * FROM orders
```

---

*URL: http://localhost:5173 | Backend: localhost:8080 | DB: XAMPP MySQL*
