#!/usr/bin/env python3
"""Generate ALL 12 Activity Diagrams as PlantUML with swimlanes."""
import os
OUT = "/Users/Study/DOAN/z pos-source-code_1/diagrams"

SKIN = """skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
"""

D = {}

D["ACT01_DangKy.puml"] = f"""@startuml
title Biểu đồ hoạt động: Đăng ký tài khoản
{SKIN}
|Người dùng mới|
start
:Chọn Đăng ký;
:Nhập thông tin đăng ký
(fullName, email, password, phone);

|Hệ thống|
:Gửi POST /auth/signup
đến AuthController;
:Kiểm tra email trong Database;

if (Email đã tồn tại?) then (Có)
  :Trả lỗi: "Email already exists";
  |Người dùng mới|
  :Hiển thị thông báo lỗi;
  stop
else (Không)
endif

if (Role = ROLE_ADMIN?) then (Có)
  :Trả lỗi: "Cannot register as Admin";
  |Người dùng mới|
  :Hiển thị thông báo lỗi;
  stop
else (Không)
endif

:Mã hóa password
bằng BCryptPasswordEncoder;
:Tạo đối tượng User mới
và lưu vào Database;
:Tạo JWT Token
(JwtProvider.generateToken);
:Trả về {{ jwt, user }};

|Người dùng mới|
:Lưu JWT vào localStorage;
:Điều hướng vào hệ thống theo role;
stop
@enduml"""

D["ACT02_DangNhap.puml"] = f"""@startuml
title Biểu đồ hoạt động: Đăng nhập
{SKIN}
|Người dùng|
start
:Chọn Đăng nhập;
:Nhập email và password;

|Hệ thống|
:Gửi POST /auth/login
đến AuthController;
:loadUserByUsername(email)
Tìm User trong Database;

if (User tồn tại?) then (Không)
  :Trả lỗi: "User not found";
  |Người dùng|
  :Hiển thị thông báo lỗi;
  stop
else (Có)
endif

:passwordEncoder.matches()
So sánh password với hash;

if (Password đúng?) then (Sai)
  :Trả lỗi: "Invalid password";
  |Người dùng|
  :Hiển thị thông báo lỗi;
  stop
else (Đúng)
endif

:Tạo JWT Token;
:Cập nhật lastLogin vào bảng users;
:Trả về {{ jwt, user }};

|Người dùng|
if (Xác định Role?) then (ADMIN)
  :Điều hướng /super-admin;
else (STORE_ADMIN)
  :Điều hướng /store;
endif
stop
@enduml"""

D["ACT03_QuenMatKhau.puml"] = f"""@startuml
title Biểu đồ hoạt động: Quên / Đặt lại mật khẩu
{SKIN}
|Người dùng|
start
:Chọn "Quên mật khẩu";
:Nhập email vào form;

|Hệ thống|
:POST /auth/forgot-password;
:Tìm User theo email trong Database;

if (Email tồn tại?) then (Không)
  :Trả lỗi: "User not found";
  |Người dùng|
  :Hiển thị thông báo lỗi;
  stop
else (Có)
endif

:Tạo UUID token (hết hạn 5 phút);
:Lưu token vào bảng password_reset_tokens;

|Email Server|
:Gửi email chứa link reset
qua Gmail SMTP;

|Người dùng|
:Nhận email, click link reset;
:Mở form nhập password mới;
:Nhập password mới và xác nhận;

|Hệ thống|
:POST /auth/reset-password
{{token, newPassword}};
:Tìm token trong Database;

if (Token còn hiệu lực?) then (Hết hạn)
  :Xóa token khỏi DB;
  :Trả lỗi: "Token expired";
  |Người dùng|
  :Hiển thị lỗi, yêu cầu gửi lại;
  stop
else (Còn)
endif

:BCrypt encode password mới;
:Cập nhật password trong bảng users;
:Xóa token đã dùng khỏi DB;

|Người dùng|
:Thông báo đổi mật khẩu thành công;
stop
@enduml"""

D["ACT04_TaoCuaHang_Duyet.puml"] = f"""@startuml
title Biểu đồ hoạt động: Tạo cửa hàng và Duyệt
{SKIN}
|Store Admin|
start
:Đăng nhập hệ thống;
:Nhập thông tin cửa hàng
(brand, description, storeType, contact);

|Hệ thống|
:POST /api/stores;
:Lấy currentUser từ JWT;
:Tạo Store với storeAdmin = currentUser;
:Set status = PENDING, createdAt = now();
:Lưu Store vào Database;
:Trả về Store (PENDING);

|Store Admin|
:Hiển thị thông báo:
"Cửa hàng đang chờ duyệt";

|Super Admin|
:Đăng nhập hệ thống;
:Xem danh sách Store có status = PENDING;
:Chọn Store cần duyệt;

if (Quyết định duyệt?) then (Approve)
  |Hệ thống|
  :PUT /stores/{{id}}/moderate
  action = APPROVE;
  :Set status = ACTIVE;
  :Lưu vào Database;
  |Store Admin|
  :Cửa hàng hoạt động
  Có thể tạo Branch, Product, Employee;
else (Block)
  |Hệ thống|
  :PUT /stores/{{id}}/moderate
  action = BLOCK;
  :Set status = BLOCKED;
  :Lưu vào Database;
  |Store Admin|
  :Cửa hàng bị chặn
  Không thể sử dụng hệ thống;
endif
stop
@enduml"""

D["ACT05_QuanLySanPham.puml"] = f"""@startuml
title Biểu đồ hoạt động: Quản lý sản phẩm
{SKIN}
|Store Admin|
start
:Chọn "Quản lý sản phẩm";

|Hệ thống|
:Tải danh sách sản phẩm của Store;
:Hiển thị danh sách sản phẩm;

|Store Admin|
:Chọn "Tạo sản phẩm mới";

|Hệ thống|
:Hiển thị form tạo sản phẩm;

|Store Admin|
:Nhập thông tin sản phẩm
(name, sku, mrp, sellingPrice,
brand, image, categoryId);

|Hệ thống|
:POST /api/products;
:checkAuthority() - Kiểm tra quyền Store Admin;

if (Có quyền?) then (Không)
  :Trả lỗi: "Unauthorized";
  |Store Admin|
  :Hiển thị thông báo lỗi;
  stop
else (Có)
endif

:Kiểm tra Category tồn tại trong Store;

if (Category hợp lệ?) then (Không)
  :Trả lỗi: "Category not found";
  |Store Admin|
  :Hiển thị thông báo lỗi;
  stop
else (Có)
endif

:Tạo Product mới (store, category);
:Lưu Product vào Database;

|Store Admin|
:Thông báo tạo sản phẩm thành công;
stop
@enduml"""

D["ACT06_ThemNhanVien.puml"] = f"""@startuml
title Biểu đồ hoạt động: Thêm nhân viên
{SKIN}
|Store Admin|
start
:Chọn "Thêm nhân viên";

|Hệ thống|
:Hiển thị form thêm nhân viên;

|Store Admin|
:Nhập thông tin nhân viên
(fullName, email, password,
phone, role, branchId);

|Hệ thống|
:POST /api/users/add-employee;
:Lấy currentUser từ JWT;
:checkAuthority() - Kiểm tra quyền;
:Kiểm tra email trùng trong Database;

if (Email đã tồn tại?) then (Có)
  :Trả lỗi: "Email already exists";
  |Store Admin|
  :Hiển thị thông báo lỗi;
  stop
else (Không)
endif

:Tìm Branch theo branchId;
:BCrypt encode password;
:Tạo User mới (role, store, branch);
:Lưu User vào Database;

|Store Admin|
:Thông báo thêm nhân viên thành công;
stop
@enduml"""

D["ACT07_BanHangPOS.puml"] = f"""@startuml
title Biểu đồ hoạt động: Luồng bán hàng POS
{SKIN}
|Cashier|
start
:Mở màn hình POS;

|Hệ thống|
:GET /api/products
Tải danh sách sản phẩm theo chi nhánh;
:Hiển thị danh sách sản phẩm;

|Cashier|
repeat
  :Tìm kiếm sản phẩm
  (theo tên hoặc mã barcode);
  :Chọn sản phẩm, nhập số lượng;

  |Hệ thống|
  :Redux: cartSlice.addItem()
  Tính subtotal, tax, total
  realtime trên Frontend;

  |Cashier|
repeat while (Thêm sản phẩm tiếp?) is (Có)
->Không;

:Chọn khách hàng (tùy chọn);
:Chọn phương thức thanh toán
(CASH / CARD / UPI);
:Nhấn nút "Thanh toán";

|Hệ thống|
:POST /api/orders;
:Lấy cashier, branch từ JWT;
:Tạo Order (status = COMPLETED,
paymentType, totalAmount);
:Lưu Order vào Database;
:Lưu từng OrderItem vào Database;
:Redux: clearCart() - Xóa giỏ hàng;

|Cashier|
:Hiển thị hóa đơn thành công;

if (In hóa đơn?) then (Có)
  :In hóa đơn;
else (Không)
endif
stop
@enduml"""

D["ACT08_TamGiu_KhoiPhuc.puml"] = f"""@startuml
title Biểu đồ hoạt động: Tạm giữ và Khôi phục đơn hàng
{SKIN}
|Cashier|
start
:Đang phục vụ khách A
Thêm sản phẩm vào giỏ hàng;
:Nhấn nút "Tạm giữ" (Hold Order);

|Hệ thống (Redux)|
:holdCurrentCart():
Lưu giỏ hiện tại vào holdOrders[];
:Tạo giỏ hàng mới (rỗng);
:Hiển thị badge số đơn tạm giữ;

|Cashier|
:Phục vụ khách hàng B
(thêm SP, thanh toán bình thường);
:Nhấn "Đơn tạm giữ" (Held Orders);

|Hệ thống (Redux)|
:getHoldOrders():
Hiển thị danh sách đơn tạm giữ;

|Cashier|
:Chọn đơn cần khôi phục;

|Hệ thống (Redux)|
:resumeHoldOrder(index):
Lấy đơn từ holdOrders[index]
Xóa khỏi danh sách
Set làm giỏ hàng hiện tại;

|Cashier|
:Giỏ hàng khách A được khôi phục;
:Tiếp tục thanh toán cho khách A;
stop
@enduml"""

D["ACT09_HoanTra.puml"] = f"""@startuml
title Biểu đồ hoạt động: Hoàn trả đơn hàng
{SKIN}
|Cashier|
start
:Chọn "Hoàn trả đơn hàng";

|Hệ thống|
:Tải danh sách đơn hàng của chi nhánh;
:Hiển thị đơn hàng có status = COMPLETED;

|Cashier|
:Chọn đơn hàng cần hoàn trả;
:Nhập lý do hoàn trả;

|Hệ thống|
:POST /api/refunds;
:Tìm Order theo orderId;

if (Order hợp lệ?) then (Không)
  :Trả lỗi: "Order không tồn tại
  hoặc đã hoàn trả";
  |Cashier|
  :Hiển thị thông báo lỗi;
  stop
else (Có)
endif

:Tạo Refund mới
(order, reason, amount,
paymentType, cashier, branch);
:Lưu Refund vào Database;
:Cập nhật Order: status = REFUNDED;
:Lưu cập nhật vào Database;

|Cashier|
:Thông báo hoàn trả thành công;
stop
@enduml"""

D["ACT10_KetThucCa.puml"] = f"""@startuml
title Biểu đồ hoạt động: Kết thúc ca làm việc
{SKIN}
|Cashier|
start
:Nhấn nút "Kết thúc ca";

|Hệ thống|
:PUT /api/shifts/{{id}}/close;
:Set shiftEnd = now();
:Query tất cả Orders trong khoảng
shiftStart đến shiftEnd;
:Query tất cả Refunds trong khoảng
shiftStart đến shiftEnd;
:Tính toán:
totalSales = SUM(orders.totalAmount)
totalRefunds = SUM(refunds.amount)
netSales = totalSales - totalRefunds
totalOrders = COUNT(orders);
:Tính PaymentSummary:
Nhóm theo CASH / CARD / UPI
Tính % và số tiền từng loại;
:Tính Top 5 sản phẩm bán chạy nhất;
:Lưu ShiftReport vào Database;
:Trả về báo cáo ca;

|Cashier|
:Hiển thị tổng kết ca:
- Tổng doanh thu
- Tổng hoàn trả
- Doanh thu thuần
- Số đơn hàng
- Top 5 SP bán chạy
- Phân bổ thanh toán;
stop
@enduml"""

D["ACT11_Subscription.puml"] = f"""@startuml
title Biểu đồ hoạt động: Đăng ký Subscription
{SKIN}
|Store Admin|
start
:Chọn "Nâng cấp gói";

|Hệ thống|
:Tải danh sách SubscriptionPlan;
:Hiển thị các gói
(BASIC, PRO, ENTERPRISE);

|Store Admin|
:Chọn gói và nhấn "Đăng ký";

|Hệ thống|
:POST /api/subscriptions/subscribe;
:Tạo Subscription (status = PENDING);
:Tạo PaymentLink qua Razorpay API;
:Trả về paymentLinkUrl;

|Store Admin|
:Redirect đến trang thanh toán;

|Razorpay|
:Hiển thị form thanh toán;

|Store Admin|
:Nhập thông tin thanh toán;

|Razorpay|
:Xử lý giao dịch;
:Callback về hệ thống
với payment_link_id và status;

|Hệ thống|
:Verify payment
GET /api/payments/verify;

if (Thanh toán thành công?) then (Có)
  :Cập nhật Subscription:
  status = ACTIVE
  startDate = now()
  endDate = now() + billingCycle;
  :Lưu Payment record vào Database;
  |Store Admin|
  :Thông báo đăng ký thành công;
else (Không)
  :Cập nhật Subscription:
  status = CANCELLED;
  |Store Admin|
  :Thông báo thanh toán thất bại;
endif
stop
@enduml"""

D["ACT12_BaoCao.puml"] = f"""@startuml
title Biểu đồ hoạt động: Xem báo cáo Analytics
{SKIN}
|Store Admin / Branch Manager|
start
:Chọn menu "Báo cáo";

|Hệ thống|
:Hiển thị trang báo cáo;

|Store Admin / Branch Manager|
:Chọn loại báo cáo
(Doanh thu / Sản phẩm / Thanh toán);
:Chọn khoảng thời gian
(Hôm nay / Tuần / Tháng / Năm);

|Hệ thống|
:GET /api/analytics/...
với params period, branch;
:Xác định timeRange từ period;
:Query Orders trong khoảng thời gian;
:Query Refunds trong khoảng thời gian;
:Tính toán aggregate:
- Tổng doanh thu
- Tổng hoàn trả
- Doanh thu thuần
- Nhóm theo ngày/tuần/tháng
- Top sản phẩm bán chạy
- Phân bổ thanh toán (CASH/CARD/UPI);
:Trả về dữ liệu báo cáo (JSON);
:Vẽ biểu đồ bằng Recharts
(BarChart, LineChart, PieChart);

|Store Admin / Branch Manager|
:Xem báo cáo trực quan;
stop
@enduml"""

for fname, content in D.items():
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(content)
    print(f"✓ {fname}")
print(f"\nDone! {len(D)} activity diagrams (PlantUML) generated.")
