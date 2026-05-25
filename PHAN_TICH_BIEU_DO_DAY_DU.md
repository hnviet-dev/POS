# 📊 PHÂN TÍCH ĐẦY ĐỦ BIỂU ĐỒ UML — HỆ THỐNG ZOSH POS

> **Chương 3.2 — Phân tích hệ thống**
> Tổng cộng: **~60+ biểu đồ** cần vẽ

---

## 3.2.1 XÁC ĐỊNH ACTOR VÀ USECASE

### 🎭 Danh sách Actor (4 actor chính + 2 hệ thống)

| # | Actor | Mô tả | Quyền chính |
|---|-------|--------|-------------|
| 1 | **Super Admin** | Quản trị viên toàn hệ thống | Duyệt/chặn cửa hàng, quản lý gói subscription |
| 2 | **Store Admin** | Chủ cửa hàng (bao gồm Store Manager) | Tạo chi nhánh, sản phẩm, nhân viên, xem báo cáo toàn store |
| 3 | **Branch Manager** | Quản lý chi nhánh (bao gồm Branch Admin) | Xem đơn hàng, tồn kho, nhân viên, báo cáo chi nhánh |
| 4 | **Cashier** | Thu ngân tại quầy | Bán hàng, tạo đơn, hoàn trả, quản lý ca |
| 5 | *(Hệ thống)* **Payment Gateway** | Razorpay/Stripe | Xử lý thanh toán subscription |
| 6 | *(Hệ thống)* **Cloudinary** | Dịch vụ lưu trữ ảnh | Upload ảnh sản phẩm |

### 📋 Danh sách UseCase theo Actor

#### Super Admin (7 UC)
| # | Mã UC | Tên UseCase |
|---|-------|-------------|
| 1 | UC-SA01 | Đăng nhập |
| 2 | UC-SA02 | Xem Dashboard tổng quan |
| 3 | UC-SA03 | Xem danh sách cửa hàng |
| 4 | UC-SA04 | Duyệt cửa hàng (Approve) |
| 5 | UC-SA05 | Chặn cửa hàng (Block) |
| 6 | UC-SA06 | Quản lý gói Subscription Plan (CRUD) |
| 7 | UC-SA07 | Xem chi tiết cửa hàng |

#### Store Admin (14 UC)
| # | Mã UC | Tên UseCase |
|---|-------|-------------|
| 1 | UC-ST01 | Đăng ký tài khoản |
| 2 | UC-ST02 | Đăng nhập |
| 3 | UC-ST03 | Tạo cửa hàng (Onboarding) |
| 4 | UC-ST04 | Cập nhật thông tin cửa hàng |
| 5 | UC-ST05 | Quản lý chi nhánh (CRUD) |
| 6 | UC-ST06 | Quản lý danh mục sản phẩm (CRUD) |
| 7 | UC-ST07 | Quản lý sản phẩm (CRUD + Upload ảnh) |
| 8 | UC-ST08 | Quản lý nhân viên (CRUD + phân quyền) |
| 9 | UC-ST09 | Đăng ký gói Subscription |
| 10 | UC-ST10 | Nâng cấp gói Subscription |
| 11 | UC-ST11 | Xem Dashboard cửa hàng |
| 12 | UC-ST12 | Xem báo cáo phân tích (Analytics) |
| 13 | UC-ST13 | Xem cảnh báo hệ thống (Alerts) |
| 14 | UC-ST14 | Quên/Đặt lại mật khẩu |

#### Branch Manager (9 UC)
| # | Mã UC | Tên UseCase |
|---|-------|-------------|
| 1 | UC-BM01 | Đăng nhập |
| 2 | UC-BM02 | Xem Dashboard chi nhánh |
| 3 | UC-BM03 | Xem danh sách đơn hàng (lọc/tìm kiếm) |
| 4 | UC-BM04 | Quản lý tồn kho (CRUD) |
| 5 | UC-BM05 | Quản lý nhân viên chi nhánh |
| 6 | UC-BM06 | Quản lý khách hàng (CRUD) |
| 7 | UC-BM07 | Xem danh sách ca làm việc |
| 8 | UC-BM08 | Xem báo cáo chi nhánh (Analytics) |
| 9 | UC-BM09 | Xem/xử lý hoàn trả |

#### Cashier (9 UC)
| # | Mã UC | Tên UseCase |
|---|-------|-------------|
| 1 | UC-CS01 | Đăng nhập |
| 2 | UC-CS02 | Bắt đầu ca làm việc (Start Shift) |
| 3 | UC-CS03 | Bán hàng tại quầy (POS) |
| 4 | UC-CS04 | Quản lý giỏ hàng (thêm/xóa/sửa số lượng) |
| 5 | UC-CS05 | Thanh toán đơn hàng (Checkout) |
| 6 | UC-CS06 | Tạm giữ đơn hàng (Hold Order) |
| 7 | UC-CS07 | Tạo hoàn trả (Refund) |
| 8 | UC-CS08 | Kết thúc ca làm việc (End Shift) |
| 9 | UC-CS09 | Xem lịch sử đơn hàng |

> **Tổng: 39 UseCase**

---

## 3.2.2 BIỂU ĐỒ USECASE TỔNG QUÁT

**1 biểu đồ** — Vẽ tất cả 4 actor chính + các nhóm chức năng lớn

```
Nhóm chức năng trên biểu đồ tổng quát:
├── Quản lý xác thực (Authentication)
├── Quản lý cửa hàng (Store Management)
├── Quản lý chi nhánh (Branch Management)
├── Quản lý sản phẩm & danh mục (Product & Category)
├── Quản lý nhân viên (Employee Management)
├── Bán hàng tại quầy (POS Sales)
├── Quản lý ca làm việc (Shift Management)
├── Quản lý hoàn trả (Refund)
├── Quản lý tồn kho (Inventory)
├── Quản lý Subscription & Thanh toán
└── Báo cáo & Phân tích (Analytics)
```

---

## 3.2.3 BIỂU ĐỒ USECASE CHI TIẾT + BẢNG ĐẶC TẢ

### Cần vẽ: **11 biểu đồ UseCase chi tiết** + **39 bảng đặc tả**

#### Biểu đồ UC chi tiết #1: Xác thực (Authentication)
- UC: Đăng ký, Đăng nhập, Quên mật khẩu, Đặt lại mật khẩu
- Actor: Tất cả
- Quan hệ: `<<include>>` Xác thực JWT

#### Biểu đồ UC chi tiết #2: Quản lý cửa hàng
- UC: Tạo cửa hàng, Cập nhật, Duyệt, Chặn, Xem danh sách
- Actor: Super Admin, Store Admin

#### Biểu đồ UC chi tiết #3: Quản lý chi nhánh
- UC: Tạo, Sửa, Xóa, Xem danh sách chi nhánh
- Actor: Store Admin

#### Biểu đồ UC chi tiết #4: Quản lý sản phẩm & danh mục
- UC: CRUD sản phẩm, CRUD danh mục, Upload ảnh, Tìm kiếm
- Actor: Store Admin
- Quan hệ: `<<include>>` Upload ảnh Cloudinary

#### Biểu đồ UC chi tiết #5: Quản lý nhân viên
- UC: Thêm nhân viên cấp Store, Thêm nhân viên cấp Branch, Phân quyền
- Actor: Store Admin, Branch Manager

#### Biểu đồ UC chi tiết #6: Bán hàng POS (⭐ Quan trọng nhất)
- UC: Thêm sản phẩm vào giỏ, Sửa số lượng, Áp dụng giảm giá, Áp dụng thuế, Chọn khách hàng, Thanh toán
- Actor: Cashier
- Quan hệ: `<<include>>` Tính tiền realtime, `<<extend>>` Tạm giữ đơn

#### Biểu đồ UC chi tiết #7: Quản lý ca làm việc
- UC: Bắt đầu ca, Kết thúc ca, Xem tiến độ ca, Xem lịch sử ca
- Actor: Cashier, Branch Manager

#### Biểu đồ UC chi tiết #8: Quản lý hoàn trả
- UC: Tạo hoàn trả, Xem danh sách hoàn trả
- Actor: Cashier, Branch Manager

#### Biểu đồ UC chi tiết #9: Quản lý tồn kho
- UC: Xem tồn kho, Cập nhật số lượng, Cảnh báo hết hàng
- Actor: Branch Manager, Store Admin

#### Biểu đồ UC chi tiết #10: Subscription & Thanh toán
- UC: Đăng ký gói, Nâng cấp gói, Thanh toán, Xác minh thanh toán
- Actor: Store Admin, Payment Gateway

#### Biểu đồ UC chi tiết #11: Báo cáo & Dashboard
- UC: Dashboard tổng quan, Báo cáo doanh thu, Top sản phẩm, Top thu ngân, Cảnh báo
- Actor: Super Admin, Store Admin, Branch Manager

---

### 📝 BẢNG ĐẶC TẢ USECASE (39 bảng — ví dụ mẫu cho các UC quan trọng)

> Mỗi UC cần 1 bảng đặc tả. Dưới đây là danh sách đầy đủ:

| # | Mã UC | Tên bảng đặc tả |
|---|-------|-----------------|
| 1 | UC-SA01 | Đặc tả UC Đăng nhập (Super Admin) |
| 2 | UC-SA02 | Đặc tả UC Xem Dashboard tổng quan |
| 3 | UC-SA03 | Đặc tả UC Xem danh sách cửa hàng |
| 4 | UC-SA04 | Đặc tả UC Duyệt cửa hàng |
| 5 | UC-SA05 | Đặc tả UC Chặn cửa hàng |
| 6 | UC-SA06 | Đặc tả UC Quản lý gói Subscription Plan |
| 7 | UC-SA07 | Đặc tả UC Xem chi tiết cửa hàng |
| 8 | UC-ST01 | Đặc tả UC Đăng ký tài khoản |
| 9 | UC-ST02 | Đặc tả UC Đăng nhập (Store Admin) |
| 10 | UC-ST03 | Đặc tả UC Tạo cửa hàng |
| 11 | UC-ST04 | Đặc tả UC Cập nhật thông tin cửa hàng |
| 12 | UC-ST05 | Đặc tả UC Quản lý chi nhánh |
| 13 | UC-ST06 | Đặc tả UC Quản lý danh mục |
| 14 | UC-ST07 | Đặc tả UC Quản lý sản phẩm |
| 15 | UC-ST08 | Đặc tả UC Quản lý nhân viên |
| 16 | UC-ST09 | Đặc tả UC Đăng ký gói Subscription |
| 17 | UC-ST10 | Đặc tả UC Nâng cấp gói Subscription |
| 18 | UC-ST11 | Đặc tả UC Xem Dashboard cửa hàng |
| 19 | UC-ST12 | Đặc tả UC Xem báo cáo phân tích |
| 20 | UC-ST13 | Đặc tả UC Xem cảnh báo |
| 21 | UC-ST14 | Đặc tả UC Quên/Đặt lại mật khẩu |
| 22 | UC-BM01 | Đặc tả UC Đăng nhập (Branch Manager) |
| 23 | UC-BM02 | Đặc tả UC Xem Dashboard chi nhánh |
| 24 | UC-BM03 | Đặc tả UC Xem danh sách đơn hàng |
| 25 | UC-BM04 | Đặc tả UC Quản lý tồn kho |
| 26 | UC-BM05 | Đặc tả UC Quản lý nhân viên chi nhánh |
| 27 | UC-BM06 | Đặc tả UC Quản lý khách hàng |
| 28 | UC-BM07 | Đặc tả UC Xem danh sách ca làm việc |
| 29 | UC-BM08 | Đặc tả UC Xem báo cáo chi nhánh |
| 30 | UC-BM09 | Đặc tả UC Xem/xử lý hoàn trả |
| 31 | UC-CS01 | Đặc tả UC Đăng nhập (Cashier) |
| 32 | UC-CS02 | Đặc tả UC Bắt đầu ca làm việc |
| 33 | UC-CS03 | Đặc tả UC Bán hàng tại quầy |
| 34 | UC-CS04 | Đặc tả UC Quản lý giỏ hàng |
| 35 | UC-CS05 | Đặc tả UC Thanh toán đơn hàng |
| 36 | UC-CS06 | Đặc tả UC Tạm giữ đơn hàng |
| 37 | UC-CS07 | Đặc tả UC Tạo hoàn trả |
| 38 | UC-CS08 | Đặc tả UC Kết thúc ca làm việc |
| 39 | UC-CS09 | Đặc tả UC Xem lịch sử đơn hàng |

---

## 3.2.4 BIỂU ĐỒ LỚP (CLASS DIAGRAM)

### Cần vẽ: **3 biểu đồ lớp**

#### Biểu đồ lớp #1: Tổng quan hệ thống (tất cả entity)
**16 lớp chính:**

| # | Lớp | Thuộc tính chính | Quan hệ |
|---|-----|-----------------|---------|
| 1 | **User** | id, fullName, email, password, phone, role, verified, lastLogin | ManyToOne → Store, ManyToOne → Branch |
| 2 | **Store** | id, brand, description, storeType, status, contact | OneToOne → User (storeAdmin), OneToMany → Branch, Product, Category |
| 3 | **StoreContact** | address, phone, email | Embedded trong Store |
| 4 | **Branch** | id, name, address, phone, email, openTime, closeTime, workingDays | ManyToOne → Store, OneToOne → User (manager) |
| 5 | **Product** | id, name, sku, description, mrp, sellingPrice, brand, image | ManyToOne → Category, ManyToOne → Store |
| 6 | **Category** | id, name | ManyToOne → Store |
| 7 | **Order** | id, totalAmount, paymentType, status, createdAt | ManyToOne → Branch, User, Customer; OneToMany → OrderItem |
| 8 | **OrderItem** | id, quantity, price | ManyToOne → Product, Order |
| 9 | **Customer** | id, fullName, email, phone | OneToMany → Order |
| 10 | **Inventory** | id, quantity, lastUpdated | ManyToOne → Branch, Product |
| 11 | **ShiftReport** | id, shiftStart, shiftEnd, totalSales, totalRefunds, netSales, totalOrders | ManyToOne → User, Branch |
| 12 | **Refund** | id, reason, amount, paymentType, createdAt | ManyToOne → Order, User, Branch, ShiftReport |
| 13 | **Subscription** | id, startDate, endDate, status, paymentGateway, paymentStatus, transactionId | ManyToOne → Store, SubscriptionPlan |
| 14 | **SubscriptionPlan** | id, name, description, price, billingCycle, maxBranches, maxUsers, maxProducts, featureFlags | OneToMany → Subscription |
| 15 | **Payment** | id, amount, provider, status, transactionId, paidAt | ManyToOne → Store, Subscription |
| 16 | **PasswordResetToken** | id, token, expiryDate | ManyToOne → User |

#### Biểu đồ lớp #2: Nhóm nghiệp vụ bán hàng (Order, OrderItem, Cart, Product, Inventory, ShiftReport, Refund)

#### Biểu đồ lớp #3: Nhóm quản trị (User, Store, Branch, Subscription, Payment)

---

## 3.2.5 BIỂU ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAM)

### Cần vẽ: **12 biểu đồ hoạt động**

| # | Tên biểu đồ | Mô tả luồng |
|---|-------------|-------------|
| 1 | **Đăng ký tài khoản** | Nhập thông tin → Kiểm tra email trùng → Mã hóa password → Tạo User → Tạo JWT → Trả về |
| 2 | **Đăng nhập** | Nhập email/pass → Tìm user → So sánh password → Tạo JWT → Điều hướng theo role |
| 3 | **Quên/Đặt lại mật khẩu** | Nhập email → Tạo token (UUID, 5 phút) → Gửi email → User click link → Nhập pass mới → Cập nhật |
| 4 | **Tạo cửa hàng & Duyệt** | Store Admin tạo store (PENDING) → Super Admin duyệt → ACTIVE |
| 5 | **Quản lý sản phẩm** | Nhập thông tin → Upload ảnh Cloudinary → Kiểm tra quyền → Lưu DB |
| 6 | **Thêm nhân viên** | Chọn role → Chọn branch (nếu cần) → Tạo user → Mã hóa pass → Gán branch/store → Lưu |
| 7 | ⭐ **Luồng bán hàng POS (quan trọng nhất)** | Mở ca → Chọn SP → Thêm giỏ → Tính tiền realtime → Chọn thanh toán → Tạo Order → Trừ kho → Xóa giỏ |
| 8 | **Tạm giữ & Khôi phục đơn** | Chọn SP → Hold → Phục vụ khách khác → Resume đơn cũ → Thanh toán |
| 9 | **Hoàn trả đơn hàng** | Chọn đơn → Nhập lý do → Tạo Refund → Cập nhật Order status = REFUNDED |
| 10 | ⭐ **Kết thúc ca làm việc** | End shift → Query orders trong ca → Query refunds → Tính totalSales, totalRefunds, netSales → Top 5 SP → Lưu report |
| 11 | **Đăng ký Subscription** | Chọn gói → Tạo Subscription → Tạo Payment → Gọi Razorpay → Redirect thanh toán → Verify callback → Kích hoạt |
| 12 | **Xem báo cáo Analytics** | Chọn loại báo cáo → Gọi API tương ứng → Query DB → Group/Aggregate → Trả JSON → Vẽ biểu đồ Recharts |

---

## 3.2.6 BIỂU ĐỒ TUẦN TỰ (SEQUENCE DIAGRAM)

### Cần vẽ: **15 biểu đồ tuần tự**

| # | Tên biểu đồ | Các đối tượng tham gia | Mô tả |
|---|-------------|----------------------|-------|
| 1 | **Đăng ký tài khoản** | User → FE(React) → AuthController → AuthService → UserRepository → DB → JwtProvider | POST /auth/signup |
| 2 | **Đăng nhập** | User → FE → AuthController → AuthService → UserDetailsService → PasswordEncoder → JwtProvider → DB | POST /auth/login |
| 3 | **Xác thực JWT (mỗi request)** | FE → JwtValidator → JwtProvider → SecurityContext → Controller → Service | Filter chain |
| 4 | **Quên mật khẩu** | User → FE → AuthController → AuthService → PasswordResetTokenRepo → EmailService → Gmail SMTP | POST /auth/forgot-password |
| 5 | **Tạo cửa hàng** | StoreAdmin → FE → Redux(storeThunks) → StoreController → StoreService → StoreRepository → DB | POST /api/stores |
| 6 | **Duyệt cửa hàng** | SuperAdmin → FE → StoreController → StoreService → DB (update status) | PUT /api/stores/{id}/moderate |
| 7 | **Tạo sản phẩm** | StoreAdmin → FE → Cloudinary(upload ảnh) → Redux → ProductController → ProductService → ProductRepository → DB | POST /api/products |
| 8 | **Thêm nhân viên** | StoreAdmin → FE → Redux → EmployeeController → EmployeeService → UserRepository → BranchRepository → DB | POST /api/employees |
| 9 | ⭐ **Bán hàng POS (quan trọng nhất)** | Cashier → FE(React) → cartSlice(Redux, local) → orderThunks → Axios → OrderController → OrderService → OrderRepository → DB | POST /api/orders |
| 10 | **Tạm giữ đơn hàng** | Cashier → FE → cartSlice(holdOrder) → cartSlice(restoreOrder) | Chỉ local Redux, không gọi API |
| 11 | ⭐ **Bắt đầu ca làm việc** | Cashier → FE → ShiftReportController → ShiftReportService → ShiftReportRepository → DB | POST /api/shift-reports/start |
| 12 | ⭐ **Kết thúc ca làm việc** | Cashier → FE → ShiftReportController → ShiftReportService → OrderRepository → RefundRepository → DB (tính toán aggregation) | PATCH /api/shift-reports/end |
| 13 | **Tạo hoàn trả** | Cashier → FE → RefundController → RefundService → OrderRepository(update status) → RefundRepository → DB | POST /api/refunds |
| 14 | **Đăng ký Subscription** | StoreAdmin → FE → SubscriptionController → SubscriptionService → PaymentService → RazorpayService → Razorpay API → Redirect | POST /api/subscriptions/subscribe |
| 15 | **Xem báo cáo Analytics** | Manager → FE → Redux(analyticsThunks) → BranchAnalyticsController → BranchAnalyticsService → OrderRepository(native query) → DB | GET /api/branch-analytics/* |

---

## 📊 TỔNG KẾT — CHECKLIST ĐẦY ĐỦ

| Mục | Nội dung | Số lượng |
|-----|---------|----------|
| **3.2.1** | Bảng xác định Actor | 1 bảng (4-6 actor) |
| **3.2.1** | Bảng liệt kê UseCase theo Actor | 4 bảng (39 UC) |
| **3.2.2** | Biểu đồ UseCase tổng quát | **1 biểu đồ** |
| **3.2.3** | Biểu đồ UseCase chi tiết | **11 biểu đồ** |
| **3.2.3** | Bảng đặc tả UseCase | **39 bảng** |
| **3.2.4** | Biểu đồ lớp | **3 biểu đồ** (tổng quan + 2 nhóm) |
| **3.2.5** | Biểu đồ hoạt động | **12 biểu đồ** |
| **3.2.6** | Biểu đồ tuần tự | **15 biểu đồ** |
| | **TỔNG CỘNG** | **~82 mục cần vẽ/viết** |

---

## 💡 GỢI Ý ƯU TIÊN

> [!IMPORTANT]
> Nếu báo cáo giới hạn số trang, hãy ưu tiên các biểu đồ có dấu ⭐. Đó là các luồng **core business** mà hội đồng sẽ hỏi nhiều nhất.

### Top 5 biểu đồ PHẢI CÓ:
1. **Biểu đồ UseCase tổng quát** — cho cái nhìn toàn cảnh
2. **Biểu đồ hoạt động: Luồng bán hàng POS** — core business
3. **Biểu đồ tuần tự: Bán hàng POS** — luồng phức tạp nhất
4. **Biểu đồ tuần tự: Kết thúc ca** — logic tính toán nặng
5. **Biểu đồ lớp tổng quan** — 16 entity + quan hệ

### Top 5 bảng đặc tả PHẢI CÓ:
1. UC-CS03: Bán hàng tại quầy
2. UC-CS05: Thanh toán đơn hàng
3. UC-CS08: Kết thúc ca làm việc
4. UC-CS07: Tạo hoàn trả
5. UC-ST07: Quản lý sản phẩm
