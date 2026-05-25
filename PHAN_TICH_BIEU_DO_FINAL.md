# 📊 PHÂN TÍCH ĐẦY ĐỦ BIỂU ĐỒ UML — HỆ THỐNG POS ĐA CHI NHÁNH (FINAL)

> Phân tích từ: 19 Controllers, 18 Entity classes, 10 Enums, 116 API endpoints, 22 Redux slices
> Tổng cộng: **~85 mục cần vẽ/viết**

---

## 3.2.1 XÁC ĐỊNH ACTOR VÀ USECASE

### 🎭 Danh sách Actor (4 chính + 2 hệ thống)

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
| 6 | UC-CS06 | Tạm giữ đơn hàng (Hold Order) — *Frontend only, không gọi API* |
| 7 | UC-CS07 | Tạo hoàn trả (Refund) |
| 8 | UC-CS08 | Kết thúc ca làm việc (End Shift) |
| 9 | UC-CS09 | Xem lịch sử đơn hàng |

> **Tổng: 39 UseCase**

---

## 3.2.2 BIỂU ĐỒ USECASE TỔNG QUÁT — 1 biểu đồ

Nhóm chức năng trên biểu đồ:
- Quản lý xác thực (Authentication)
- Quản lý cửa hàng (Store Management)
- Quản lý chi nhánh (Branch Management)
- Quản lý sản phẩm & danh mục
- Quản lý nhân viên
- Bán hàng tại quầy (POS Sales)
- Quản lý ca làm việc (Shift)
- Quản lý hoàn trả (Refund)
- Quản lý tồn kho (Inventory)
- Quản lý khách hàng (Customer)
- Quản lý Subscription & Thanh toán
- Báo cáo & Phân tích (Analytics)

---

## 3.2.3 BIỂU ĐỒ USECASE CHI TIẾT — 11 biểu đồ + 39 bảng đặc tả

| # | Biểu đồ UC chi tiết | Actor | UC bên trong |
|---|---------------------|-------|-------------|
| 1 | Xác thực | Tất cả | Đăng ký, Đăng nhập, Quên MK, Đặt lại MK |
| 2 | Quản lý cửa hàng | Super Admin, Store Admin | Tạo, Cập nhật, Duyệt, Chặn, Xem DS |
| 3 | Quản lý chi nhánh | Store Admin | Tạo, Sửa, Xóa, Xem DS |
| 4 | Quản lý sản phẩm & danh mục | Store Admin | CRUD SP, CRUD danh mục, Upload ảnh, Tìm kiếm |
| 5 | Quản lý nhân viên | Store Admin, Branch Manager | Thêm cấp Store, Thêm cấp Branch, Phân quyền |
| 6 | ⭐ Bán hàng POS | Cashier | Thêm SP giỏ, Sửa SL, Giảm giá, Thuế, Chọn KH, Thanh toán |
| 7 | Quản lý ca làm việc | Cashier, Branch Manager | Start/End shift, Xem tiến độ, Xem lịch sử |
| 8 | Quản lý hoàn trả | Cashier, Branch Manager | Tạo hoàn trả, Xem DS hoàn trả |
| 9 | Quản lý tồn kho | Branch Manager, Store Admin | Xem, Cập nhật SL, Cảnh báo hết hàng |
| 10 | Subscription & Thanh toán | Store Admin, Payment Gateway | Đăng ký gói, Nâng cấp, Thanh toán, Xác minh |
| 11 | Báo cáo & Dashboard | Super Admin, Store Admin, Branch Mgr | Dashboard, Doanh thu, Top SP, Top cashier, Cảnh báo |

### 39 bảng đặc tả:
| # | Mã | Tên | # | Mã | Tên |
|---|-----|-----|---|-----|-----|
| 1 | UC-SA01 | Đăng nhập (SA) | 21 | UC-ST14 | Quên/Đặt lại MK |
| 2 | UC-SA02 | Xem Dashboard | 22 | UC-BM01 | Đăng nhập (BM) |
| 3 | UC-SA03 | Xem DS store | 23 | UC-BM02 | Dashboard chi nhánh |
| 4 | UC-SA04 | Duyệt store | 24 | UC-BM03 | Xem đơn hàng |
| 5 | UC-SA05 | Chặn store | 25 | UC-BM04 | QL tồn kho |
| 6 | UC-SA06 | QL Subscription Plan | 26 | UC-BM05 | QL NV chi nhánh |
| 7 | UC-SA07 | Xem chi tiết store | 27 | UC-BM06 | QL khách hàng |
| 8 | UC-ST01 | Đăng ký TK | 28 | UC-BM07 | Xem DS ca |
| 9 | UC-ST02 | Đăng nhập (ST) | 29 | UC-BM08 | Báo cáo chi nhánh |
| 10 | UC-ST03 | Tạo cửa hàng | 30 | UC-BM09 | Xem hoàn trả |
| 11 | UC-ST04 | Cập nhật store | 31 | UC-CS01 | Đăng nhập (CS) |
| 12 | UC-ST05 | QL chi nhánh | 32 | UC-CS02 | Start Shift |
| 13 | UC-ST06 | QL danh mục | 33 | UC-CS03 | Bán hàng POS |
| 14 | UC-ST07 | QL sản phẩm | 34 | UC-CS04 | QL giỏ hàng |
| 15 | UC-ST08 | QL nhân viên | 35 | UC-CS05 | Thanh toán |
| 16 | UC-ST09 | Đăng ký gói | 36 | UC-CS06 | Tạm giữ đơn |
| 17 | UC-ST10 | Nâng cấp gói | 37 | UC-CS07 | Hoàn trả |
| 18 | UC-ST11 | Dashboard store | 38 | UC-CS08 | End Shift |
| 19 | UC-ST12 | Báo cáo analytics | 39 | UC-CS09 | Lịch sử đơn |
| 20 | UC-ST13 | Cảnh báo | | | |

---

## 3.2.4 BIỂU ĐỒ LỚP (CLASS DIAGRAM) — 3 biểu đồ

### Biểu đồ lớp #1: Tổng quan — 18 lớp chính

| # | Lớp | Thuộc tính chính | Quan hệ |
|---|-----|-----------------|---------|
| 1 | **User** | id, fullName, email, password, phone, role, verified, lastLogin | ManyToOne → Store, Branch |
| 2 | **Store** | id, brand, description, storeType, status, contact | OneToOne → User (storeAdmin) |
| 3 | **StoreContact** | address, phone, email | Embedded trong Store |
| 4 | **Branch** | id, name, address, phone, email, openTime, closeTime, workingDays | ManyToOne → Store, User (manager) |
| 5 | **Product** | id, name, sku, description, mrp, sellingPrice, brand, image | ManyToOne → Category, Store |
| 6 | **Category** | id, name | ManyToOne → Store |
| 7 | **Order** | id, totalAmount, paymentType, status, createdAt | ManyToOne → Branch, User, Customer; OneToMany → OrderItem |
| 8 | **OrderItem** | id, quantity, price | ManyToOne → Product, Order |
| 9 | **Customer** | id, fullName, email, phone | Standalone |
| 10 | **Inventory** | id, quantity, lastUpdated | ManyToOne → Branch, Product |
| 11 | **ShiftReport** | id, shiftStart, shiftEnd, totalSales, totalRefunds, netSales, totalOrders | ManyToOne → User, Branch; OneToMany → Refund, PaymentSummary |
| 12 | **Refund** | id, reason, amount, paymentType, createdAt | ManyToOne → Order, User, Branch, ShiftReport |
| 13 | **Subscription** | id, startDate, endDate, status, paymentGateway, paymentStatus, transactionId | ManyToOne → Store, SubscriptionPlan |
| 14 | **SubscriptionPlan** | id, name, description, price, billingCycle, maxBranches, maxUsers, maxProducts, featureFlags | OneToMany → Subscription |
| 15 | **Payment** | id, amount, provider, status, transactionId, paidAt | ManyToOne → Store; OneToOne → Subscription |
| 16 | **PaymentOrder** | id, amount, status, paymentLinkId, planId | ManyToOne → User |
| 17 | **PaymentSummary** | type, totalAmount, transactionCount, percentage | Embedded trong ShiftReport |
| 18 | **PasswordResetToken** | id, token, expiryDate | ManyToOne → User |

### Enums (8 enum):
| Enum | Giá trị |
|------|--------|
| UserRole | ROLE_ADMIN, ROLE_STORE_ADMIN, ROLE_STORE_MANAGER, ROLE_BRANCH_MANAGER, ROLE_BRANCH_ADMIN, ROLE_BRANCH_CASHIER, ROLE_CUSTOMER |
| OrderStatus | COMPLETED, PENDING, REFUNDED, CANCELLED |
| PaymentType | CASH, CARD, UPI |
| StoreStatus | PENDING, ACTIVE, BLOCKED |
| SubscriptionStatus | TRIAL, ACTIVE, EXPIRED, CANCELLED |
| PaymentStatus | PENDING, SUCCESS, FAILED |
| BillingCycle | MONTHLY, YEARLY |
| PaymentGateway | RAZORPAY, STRIPE |

### Biểu đồ lớp #2: Nhóm nghiệp vụ bán hàng
Order, OrderItem, Product, Category, Inventory, ShiftReport, Refund, PaymentSummary, Customer

### Biểu đồ lớp #3: Nhóm quản trị
User, Store, StoreContact, Branch, Subscription, SubscriptionPlan, Payment, PaymentOrder, PasswordResetToken

---

## 3.2.5 BIỂU ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAM) — 13 biểu đồ

| # | Tên biểu đồ | Mô tả luồng | Actor |
|---|-------------|-------------|-------|
| 1 | **Đăng ký tài khoản** | Nhập thông tin → Kiểm tra email trùng → Mã hóa BCrypt → Tạo User → Tạo JWT → Trả về | Store Admin mới |
| 2 | **Đăng nhập** | Nhập email/pass → Tìm user → So sánh BCrypt → Tạo JWT → Điều hướng theo role | Tất cả |
| 3 | **Quên/Đặt lại mật khẩu** | Nhập email → Tạo token UUID (5 phút) → Gửi email Gmail SMTP → Click link → Nhập pass mới → BCrypt hash → Cập nhật | Tất cả |
| 4 | **Tạo cửa hàng & Duyệt** | Store Admin tạo store (PENDING) → Super Admin xem pending → Approve → ACTIVE | Store Admin, Super Admin |
| 5 | **Quản lý sản phẩm** | Nhập thông tin → Upload ảnh Cloudinary → Kiểm tra quyền checkAuthority() → Lưu DB | Store Admin |
| 6 | **Thêm nhân viên** | Chọn role → Chọn branch (nếu cần) → Tạo user → Mã hóa pass → Gán branch/store → Lưu | Store Admin |
| 7 | ⭐ **Luồng bán hàng POS** | Mở ca → Tìm SP → Thêm giỏ → Tính tiền realtime → Chọn thanh toán CASH/CARD/UPI → Tạo Order → Xóa giỏ | Cashier |
| 8 | **Tạm giữ & Khôi phục đơn** | Chọn SP → Hold → Phục vụ khách khác → Resume đơn cũ → Thanh toán | Cashier |
| 9 | **Hoàn trả đơn hàng** | Chọn đơn → Nhập lý do → Tạo Refund → Cập nhật Order status = REFUNDED | Cashier |
| 10 | ⭐ **Kết thúc ca làm việc** | End shift → Query orders trong ca → Query refunds → Tính totalSales, totalRefunds, netSales → Top 5 SP → Lưu report | Cashier |
| 11 | **Đăng ký Subscription** | Chọn gói → Tạo Subscription → Tạo Payment → Gọi Razorpay → Redirect → Verify callback → Kích hoạt | Store Admin |
| 12 | **Xem báo cáo Analytics** | Chọn loại báo cáo → Gọi API → Query DB → Group/Aggregate → Trả JSON → Vẽ Recharts | Store Admin, Branch Mgr |
| 13 | **Quản lý tồn kho chi nhánh** | Xem tồn kho → Cập nhật số lượng → Kiểm tra min_stock → Hiển thị cảnh báo nếu thấp | Branch Manager |

---

## 3.2.6 BIỂU ĐỒ TUẦN TỰ (SEQUENCE DIAGRAM) — 17 biểu đồ

| # | Tên biểu đồ | Đối tượng tham gia | API |
|---|-------------|-------------------|-----|
| 1 | **Đăng ký tài khoản** | User → FE → AuthController → AuthService → UserRepo → BCrypt → JwtProvider → DB | POST /auth/signup |
| 2 | **Đăng nhập** | User → FE → AuthController → AuthService → UserDetailsService → PasswordEncoder → JwtProvider → DB | POST /auth/login |
| 3 | **Xác thực JWT (mỗi request)** | FE → JwtValidator → JwtProvider → SecurityContext → Controller → Service | Filter chain |
| 4 | **Quên mật khẩu** | User → FE → AuthController → AuthService → PasswordResetTokenRepo → EmailService → Gmail SMTP | POST /auth/forgot-password |
| 5 | **Tạo cửa hàng** | StoreAdmin → FE → Redux(storeThunks) → StoreController → StoreService → StoreRepo → DB | POST /api/stores |
| 6 | **Duyệt/Chặn cửa hàng** | SuperAdmin → FE → StoreController → StoreService → DB (update status) | PUT /api/stores/{id}/moderate |
| 7 | **Tạo sản phẩm** | StoreAdmin → FE → Cloudinary(upload ảnh) → Redux → ProductController → ProductService → ProductRepo → DB | POST /api/products |
| 8 | **Thêm nhân viên** | StoreAdmin → FE → Redux → EmployeeController → EmployeeService → UserRepo → BranchRepo → DB | POST /api/employees |
| 9 | ⭐ **Bán hàng POS** | Cashier → FE → cartSlice(Redux local) → orderThunks → Axios → OrderController → OrderService → OrderRepo → DB | POST /api/orders |
| 10 | **Tạm giữ đơn hàng** | Cashier → FE → cartSlice(holdOrder) → cartSlice(restoreOrder) | *Chỉ local Redux, không gọi API* |
| 11 | ⭐ **Bắt đầu ca** | Cashier → FE → ShiftReportController → ShiftReportService → ShiftReportRepo → DB | POST /api/shift-reports/start |
| 12 | ⭐ **Kết thúc ca** | Cashier → FE → ShiftReportController → ShiftReportService → OrderRepo → RefundRepo → DB (aggregation) | PATCH /api/shift-reports/end |
| 13 | **Tạo hoàn trả** | Cashier → FE → RefundController → RefundService → OrderRepo(update status) → RefundRepo → DB | POST /api/refunds |
| 14 | **Đăng ký Subscription** | StoreAdmin → FE → SubscriptionController → SubscriptionService → PaymentService → Razorpay API → Redirect | POST /api/subscriptions/subscribe |
| 15 | **Xem báo cáo Analytics** | Manager → FE → Redux → AnalyticsController → AnalyticsService → OrderRepo(query) → DB → Charts | GET /api/store/analytics/* |
| 16 | **Quản lý tồn kho** | BranchMgr → FE → Redux → InventoryController → InventoryService → InventoryRepo → DB | POST/PUT/GET /api/inventories/* |
| 17 | **Quản lý khách hàng** | Cashier/BranchMgr → FE → Redux → CustomerController → CustomerService → CustomerRepo → DB | CRUD /api/customers/* |

---

## 📊 TỔNG KẾT CUỐI CÙNG — CHECKLIST

| Mục | Nội dung | Số lượng |
|-----|---------|----------|
| **3.2.1** | Bảng xác định Actor | 1 bảng (6 actor) |
| **3.2.1** | Bảng liệt kê UseCase theo Actor | 4 bảng (39 UC) |
| **3.2.2** | Biểu đồ UseCase tổng quát | **1 biểu đồ** |
| **3.2.3** | Biểu đồ UseCase chi tiết | **11 biểu đồ** |
| **3.2.3** | Bảng đặc tả UseCase | **39 bảng** |
| **3.2.4** | Biểu đồ lớp | **3 biểu đồ** (18 class + 8 enum) |
| **3.2.5** | Biểu đồ hoạt động | **13 biểu đồ** |
| **3.2.6** | Biểu đồ tuần tự | **17 biểu đồ** |
| | **TỔNG CỘNG** | **~85 mục cần vẽ/viết** |

---

## 💡 GỢI Ý ƯU TIÊN

### Top 5 biểu đồ PHẢI CÓ (hội đồng sẽ hỏi):
1. ⭐ **UseCase tổng quát** — cái nhìn toàn cảnh
2. ⭐ **Activity: Luồng bán hàng POS** — core business
3. ⭐ **Sequence: Bán hàng POS** — luồng phức tạp nhất
4. ⭐ **Sequence: Kết thúc ca** — logic tính toán nặng
5. ⭐ **Class Diagram tổng quan** — 18 entity + quan hệ

### Top 5 bảng đặc tả PHẢI CÓ:
1. UC-CS03: Bán hàng tại quầy
2. UC-CS05: Thanh toán đơn hàng
3. UC-CS08: Kết thúc ca làm việc
4. UC-CS07: Tạo hoàn trả
5. UC-ST07: Quản lý sản phẩm

---

## 🎯 THỨ TỰ LÀM

Gõ cho tôi theo thứ tự, ví dụ: "làm UC tổng quát", "làm Activity đăng nhập"...

| Bước | Việc cần làm |
|------|-------------|
| 1 | UC tổng quát |
| 2 | 11 UC chi tiết + 39 bảng đặc tả |
| 3 | 3 Class Diagram |
| 4 | 13 Activity Diagram |
| 5 | 17 Sequence Diagram |
