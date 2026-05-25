#!/usr/bin/env python3
"""Generate remaining PlantUML Sequence Diagrams (8-17)."""
import os
OUT = "/Users/Study/DOAN/z pos-source-code_1/diagrams"

SKIN = """skinparam shadowing false
skinparam sequence {
    ArrowColor black
    LifeLineBorderColor black
    LifeLineBackgroundColor white
    ParticipantBorderColor black
    ParticipantBackgroundColor white
}
"""

D = {}

# ====== 8. Tạo chi nhánh ======
D["SEQ08_TaoChiNhanh.puml"] = f"""@startuml
title Biểu đồ tuần tự: Tạo chi nhánh
{SKIN}
actor "Store Admin" as user
boundary "Form_TaoChiNhanh" as bd
control "Control_Branch" as ctrl
entity "Entity_Branch" as ent
entity "Entity_Store" as store
database "CSDL" as db

user -> bd : Chọn "Tạo chi nhánh"
activate bd
bd --> user : Hiển thị form tạo chi nhánh
user -> bd : Nhập thông tin\\n(name, address, phone, email,\\nopenTime, closeTime, workingDays)
bd -> ctrl : POST /api/branches
activate ctrl

ctrl -> ctrl : Lấy currentUser từ JWT
ctrl -> store : getStoreByUser(currentUser)
activate store
store -> db : SELECT * FROM stores\\nWHERE store_admin_id=?
activate db
db --> store : Store
deactivate db
store --> ctrl : Store
deactivate store

ctrl -> ctrl : checkAuthority()\\nKiểm tra quyền Store Admin

alt Không có quyền
    ctrl --> bd : Lỗi: "Unauthorized"
    bd --> user : Hiển thị lỗi
else Có quyền
    ctrl -> ent : Tạo Branch mới\\n(store = currentStore)
    activate ent
    ent -> db : INSERT INTO branches(...)
    activate db
    db --> ent : Branch ID
    deactivate db
    ent --> ctrl : Branch đã tạo
    deactivate ent
    ctrl --> bd : Trả về Branch
    deactivate ctrl
    bd --> user : Thông báo tạo chi nhánh thành công
end
deactivate bd
@enduml"""

# ====== 9. Tạo sản phẩm ======
D["SEQ09_TaoSanPham.puml"] = f"""@startuml
title Biểu đồ tuần tự: Tạo sản phẩm
{SKIN}
actor "Store Admin" as user
boundary "Form_TaoSanPham" as bd
control "Control_Product" as ctrl
entity "Entity_Product" as prod
entity "Entity_Category" as cat
entity "Entity_Store" as store
database "CSDL" as db

user -> bd : Chọn "Tạo sản phẩm"
activate bd
bd --> user : Hiển thị form tạo sản phẩm
user -> bd : Nhập thông tin sản phẩm\\n(name, sku, description, mrp,\\nsellingPrice, brand, image, categoryId)
bd -> ctrl : POST /api/products
activate ctrl

ctrl -> ctrl : Lấy currentUser từ JWT
ctrl -> store : getStoreByUser(currentUser)
activate store
store -> db : SELECT * FROM stores WHERE store_admin_id=?
activate db
db --> store : Store
deactivate db
store --> ctrl : Store
deactivate store

ctrl -> ctrl : checkAuthority()

ctrl -> cat : findById(categoryId)
activate cat
cat -> db : SELECT * FROM categories WHERE id=?
activate db
db --> cat : Category
deactivate db
cat --> ctrl : Category
deactivate cat

alt Category không tồn tại
    ctrl --> bd : Lỗi: "Category not found"
    bd --> user : Hiển thị lỗi
else Category hợp lệ
    ctrl -> prod : Tạo Product mới\\n(store, category)
    activate prod
    prod -> db : INSERT INTO products(...)
    activate db
    db --> prod : Product ID
    deactivate db
    prod --> ctrl : Product đã tạo
    deactivate prod
    ctrl --> bd : Trả về Product
    deactivate ctrl
    bd --> user : Thông báo tạo sản phẩm thành công
end
deactivate bd
@enduml"""

# ====== 10. Tạo danh mục ======
D["SEQ10_TaoDanhMuc.puml"] = f"""@startuml
title Biểu đồ tuần tự: Tạo danh mục sản phẩm
{SKIN}
actor "Store Admin" as user
boundary "Form_TaoDanhMuc" as bd
control "Control_Category" as ctrl
entity "Entity_Category" as ent
entity "Entity_Store" as store
database "CSDL" as db

user -> bd : Chọn "Tạo danh mục"
activate bd
bd --> user : Hiển thị form tạo danh mục
user -> bd : Nhập tên danh mục
bd -> ctrl : POST /api/categories
activate ctrl

ctrl -> ctrl : Lấy currentUser từ JWT
ctrl -> store : getStoreByUser(currentUser)
activate store
store -> db : SELECT * FROM stores WHERE store_admin_id=?
activate db
db --> store : Store
deactivate db
store --> ctrl : Store
deactivate store

ctrl -> ent : Tạo Category mới\\n(name, store)
activate ent
ent -> db : INSERT INTO categories(...)
activate db
db --> ent : Category ID
deactivate db
ent --> ctrl : Category đã tạo
deactivate ent

ctrl --> bd : Trả về Category
deactivate ctrl
bd --> user : Thông báo tạo danh mục thành công
deactivate bd
@enduml"""

# ====== 11. Thêm nhân viên ======
D["SEQ11_ThemNhanVien.puml"] = f"""@startuml
title Biểu đồ tuần tự: Thêm nhân viên
{SKIN}
actor "Store Admin" as admin
boundary "Form_ThemNV" as bd
control "Control_User" as ctrl
entity "Entity_User" as ent
entity "Entity_Branch" as branch
database "CSDL" as db

admin -> bd : Chọn "Thêm nhân viên"
activate bd
bd --> admin : Hiển thị form thêm nhân viên
admin -> bd : Nhập thông tin\\n(fullName, email, password,\\nphone, role, branchId)
bd -> ctrl : POST /api/users/add-employee
activate ctrl

ctrl -> ctrl : Lấy currentUser từ JWT\\nKiểm tra quyền Store Admin

ctrl -> ent : findByEmail(email)
activate ent
ent -> db : SELECT * FROM users WHERE email=?
activate db
db --> ent : Kết quả
deactivate db
ent --> ctrl : Kết quả
deactivate ent

alt Email đã tồn tại
    ctrl --> bd : Lỗi: "Email already exists"
    bd --> admin : Hiển thị lỗi
else Email chưa tồn tại
    ctrl -> branch : findById(branchId)
    activate branch
    branch -> db : SELECT * FROM branches WHERE id=?
    activate db
    db --> branch : Branch
    deactivate db
    branch --> ctrl : Branch
    deactivate branch

    ctrl -> ctrl : BCrypt encode password
    ctrl -> ent : Tạo User mới\\n(role, store, branch)
    activate ent
    ent -> db : INSERT INTO users(...)
    activate db
    db --> ent : User ID
    deactivate db
    ent --> ctrl : User đã tạo
    deactivate ent

    ctrl --> bd : Trả về User
    deactivate ctrl
    bd --> admin : Thông báo thêm nhân viên thành công
end
deactivate bd
@enduml"""

# ====== 12. Tạm giữ & Khôi phục đơn hàng ======
D["SEQ12_TamGiu_KhoiPhuc.puml"] = f"""@startuml
title Biểu đồ tuần tự: Tạm giữ và Khôi phục đơn hàng
{SKIN}
actor "Cashier" as user
boundary "ManHinh_POS" as bd
control "Control_Cart" as ctrl

== Giai đoạn 1: Tạm giữ đơn hàng ==
user -> bd : Thêm sản phẩm vào giỏ hàng
activate bd
bd -> ctrl : Redux: addItemToCart()
activate ctrl
ctrl -> ctrl : Cập nhật cartSlice state\\n(items, subtotal, total)
ctrl --> bd : Giỏ hàng đã cập nhật
deactivate ctrl
bd --> user : Hiển thị giỏ hàng

user -> bd : Nhấn "Tạm giữ" (Hold)
bd -> ctrl : Redux: holdCurrentCart()
activate ctrl
ctrl -> ctrl : Lưu giỏ hàng hiện tại\\nvào holdOrders[]\\n(lưu trong Redux state)
ctrl -> ctrl : Tạo giỏ hàng mới (rỗng)
ctrl --> bd : Giỏ mới + badge hold count
deactivate ctrl
bd --> user : Hiển thị giỏ hàng mới\\n(giỏ cũ đã được tạm giữ)

== Giai đoạn 2: Phục vụ khách tiếp theo ==
user -> bd : Phục vụ khách hàng khác\\n(thêm SP, thanh toán bình thường)
bd --> user : Xử lý đơn hàng mới

== Giai đoạn 3: Khôi phục đơn tạm giữ ==
user -> bd : Nhấn "Đơn tạm giữ" (Held Orders)
bd -> ctrl : Redux: getHoldOrders()
activate ctrl
ctrl --> bd : Danh sách đơn tạm giữ
deactivate ctrl
bd --> user : Hiển thị danh sách đơn tạm giữ

user -> bd : Chọn đơn cần khôi phục
bd -> ctrl : Redux: resumeHoldOrder(index)
activate ctrl
ctrl -> ctrl : Lấy đơn từ holdOrders[index]\\nXóa khỏi holdOrders[]\\nSet làm giỏ hàng hiện tại
ctrl --> bd : Giỏ hàng đã khôi phục
deactivate ctrl
bd --> user : Hiển thị giỏ hàng cũ\\n→ Tiếp tục thanh toán
deactivate bd
@enduml"""

# ====== 13. Hoàn trả đơn hàng ======
D["SEQ13_HoanTra.puml"] = f"""@startuml
title Biểu đồ tuần tự: Hoàn trả đơn hàng
{SKIN}
actor "Cashier" as user
boundary "ManHinh_HoanTra" as bd
control "Control_Refund" as ctrl
entity "Entity_Refund" as ref
entity "Entity_Order" as ord
database "CSDL" as db

user -> bd : Chọn "Hoàn trả"
activate bd
bd -> ctrl : GET /api/orders?branch=...
activate ctrl
ctrl -> ord : Lấy danh sách đơn hàng
activate ord
ord -> db : SELECT * FROM orders\\nWHERE branch_id=?
activate db
db --> ord : List<Order>
deactivate db
ord --> ctrl : Danh sách đơn
deactivate ord
ctrl --> bd : Trả danh sách
deactivate ctrl
bd --> user : Hiển thị danh sách đơn hàng

user -> bd : Chọn đơn hàng cần hoàn trả
user -> bd : Nhập lý do hoàn trả
bd -> ctrl : POST /api/refunds
activate ctrl

ctrl -> ctrl : Lấy cashier từ JWT
ctrl -> ord : findById(orderId)
activate ord
ord -> db : SELECT * FROM orders WHERE id=?
activate db
db --> ord : Order
deactivate db
ord --> ctrl : Order
deactivate ord

alt Order không tồn tại hoặc đã REFUNDED
    ctrl --> bd : Lỗi: "Order not found\\nhoặc đã hoàn trả"
    bd --> user : Hiển thị lỗi
else Order hợp lệ
    ctrl -> ref : Tạo Refund mới\\n(order, reason, amount,\\npaymentType, cashier, branch)
    activate ref
    ref -> db : INSERT INTO refunds(...)
    activate db
    db --> ref : Refund ID
    deactivate db
    ref --> ctrl : Refund đã tạo
    deactivate ref

    ctrl -> ord : Cập nhật Order\\nstatus = REFUNDED
    activate ord
    ord -> db : UPDATE orders SET status='REFUNDED'
    activate db
    db --> ord : OK
    deactivate db
    ord --> ctrl : OK
    deactivate ord

    ctrl --> bd : Trả về Refund
    deactivate ctrl
    bd --> user : Thông báo hoàn trả thành công
end
deactivate bd
@enduml"""

# ====== 14. Đăng ký Subscription ======
D["SEQ14_Subscription.puml"] = f"""@startuml
title Biểu đồ tuần tự: Đăng ký Subscription
{SKIN}
actor "Store Admin" as user
boundary "ManHinh_Subscription" as bd
control "Control_Subscription" as ctrl
entity "Entity_Subscription" as sub
entity "Entity_Plan" as plan
entity "Entity_Payment" as pay
database "CSDL" as db

user -> bd : Chọn "Nâng cấp gói"
activate bd
bd -> ctrl : GET /api/plans
activate ctrl
ctrl -> plan : Lấy tất cả SubscriptionPlan
activate plan
plan -> db : SELECT * FROM subscription_plans
activate db
db --> plan : List<Plan>
deactivate db
plan --> ctrl : Danh sách gói
deactivate plan
ctrl --> bd : Trả danh sách gói
deactivate ctrl
bd --> user : Hiển thị các gói\\n(BASIC, PRO, ENTERPRISE)

user -> bd : Chọn gói và nhấn "Đăng ký"
bd -> ctrl : POST /api/subscriptions/subscribe
activate ctrl

ctrl -> ctrl : Lấy Store từ currentUser
ctrl -> sub : Tạo Subscription mới\\n(store, plan, status=PENDING)
activate sub
sub -> db : INSERT INTO subscriptions(...)
activate db
db --> sub : Subscription ID
deactivate db
sub --> ctrl : Subscription
deactivate sub

ctrl -> ctrl : Tạo PaymentLink qua Razorpay API
ctrl -> pay : Tạo PaymentOrder\\n(amount, paymentLinkId)
activate pay
pay -> db : INSERT INTO payment_orders(...)
activate db
db --> pay : OK
deactivate db
pay --> ctrl : PaymentOrder
deactivate pay

ctrl --> bd : Trả về paymentLinkUrl
deactivate ctrl
bd --> user : Redirect đến trang thanh toán Razorpay

user -> bd : Hoàn tất thanh toán trên Razorpay
bd -> ctrl : Razorpay callback\\nGET /api/payments/verify?\\npayment_link_id=...&status=...
activate ctrl

alt Thanh toán thành công
    ctrl -> sub : Cập nhật Subscription\\nstatus = ACTIVE\\nstartDate, endDate
    activate sub
    sub -> db : UPDATE subscriptions\\nSET status='ACTIVE'
    activate db
    db --> sub : OK
    deactivate db
    sub --> ctrl : OK
    deactivate sub

    ctrl -> pay : Lưu Payment record
    activate pay
    pay -> db : INSERT INTO payments(...)
    activate db
    db --> pay : OK
    deactivate db
    pay --> ctrl : OK
    deactivate pay

    ctrl --> bd : Thành công
    bd --> user : Thông báo đăng ký thành công
else Thanh toán thất bại
    ctrl -> sub : status = CANCELLED
    activate sub
    sub -> db : UPDATE subscriptions SET status='CANCELLED'
    activate db
    db --> sub : OK
    deactivate db
    sub --> ctrl : OK
    deactivate sub
    ctrl --> bd : Lỗi thanh toán
    bd --> user : Thông báo thanh toán thất bại
end
deactivate ctrl
deactivate bd
@enduml"""

# ====== 15. Xem báo cáo Analytics ======
D["SEQ15_BaoCao.puml"] = f"""@startuml
title Biểu đồ tuần tự: Xem báo cáo Analytics
{SKIN}
actor "Store Admin /\\nBranch Manager" as user
boundary "ManHinh_BaoCao" as bd
control "Control_Analytics" as ctrl
entity "Entity_Order" as ord
entity "Entity_Refund" as ref
database "CSDL" as db

user -> bd : Chọn "Báo cáo"
activate bd
bd --> user : Hiển thị trang báo cáo\\n(chọn loại, khoảng thời gian)

user -> bd : Chọn loại báo cáo\\n(Doanh thu / Sản phẩm / Thanh toán)
user -> bd : Chọn khoảng thời gian\\n(Hôm nay / Tuần / Tháng / Năm)
bd -> ctrl : GET /api/analytics/...\\n?period=...&branch=...
activate ctrl

ctrl -> ctrl : Xác định timeRange\\ntừ period parameter

ctrl -> ord : Lấy orders trong khoảng thời gian
activate ord
ord -> db : SELECT * FROM orders\\nWHERE createdAt BETWEEN ? AND ?\\nAND branch_id=?
activate db
db --> ord : List<Order>
deactivate db
ord --> ctrl : Danh sách đơn hàng
deactivate ord

ctrl -> ref : Lấy refunds trong khoảng thời gian
activate ref
ref -> db : SELECT * FROM refunds\\nWHERE createdAt BETWEEN ? AND ?
activate db
db --> ref : List<Refund>
deactivate db
ref --> ctrl : Danh sách hoàn trả
deactivate ref

ctrl -> ctrl : Tính toán aggregate:\\n- Tổng doanh thu\\n- Tổng hoàn trả\\n- Doanh thu thuần\\n- Nhóm theo ngày/tuần/tháng\\n- Top sản phẩm bán chạy\\n- Phân bổ thanh toán (CASH/CARD/UPI)

ctrl --> bd : Trả về dữ liệu báo cáo (JSON)
deactivate ctrl
bd -> bd : Vẽ biểu đồ bằng Recharts\\n(BarChart, LineChart, PieChart)
bd --> user : Hiển thị báo cáo trực quan
deactivate bd
@enduml"""

# ====== 16. Quản lý tồn kho ======
D["SEQ16_TonKho.puml"] = f"""@startuml
title Biểu đồ tuần tự: Quản lý tồn kho chi nhánh
{SKIN}
actor "Branch Manager" as user
boundary "ManHinh_TonKho" as bd
control "Control_Inventory" as ctrl
entity "Entity_Inventory" as inv
entity "Entity_Branch" as branch
database "CSDL" as db

user -> bd : Chọn "Quản lý tồn kho"
activate bd
bd -> ctrl : GET /api/inventory?branch=...
activate ctrl
ctrl -> ctrl : Lấy branch từ currentUser
ctrl -> inv : Lấy inventory theo branch
activate inv
inv -> db : SELECT i.*, p.name FROM inventory i\\nJOIN products p ON i.product_id=p.id\\nWHERE i.branch_id=?
activate db
db --> inv : List<Inventory>
deactivate db
inv --> ctrl : Danh sách tồn kho
deactivate inv
ctrl --> bd : Trả danh sách
deactivate ctrl
bd --> user : Hiển thị bảng tồn kho\\n(SP, số lượng, cảnh báo thấp)

user -> bd : Chọn sản phẩm\\nNhập số lượng mới
bd -> ctrl : PUT /api/inventory/{{id}}
activate ctrl

ctrl -> inv : findById(inventoryId)
activate inv
inv -> db : SELECT * FROM inventory WHERE id=?
activate db
db --> inv : Inventory
deactivate db
inv --> ctrl : Inventory
deactivate inv

ctrl -> ctrl : Kiểm tra quyền\\n(branch của user = branch của inventory)

alt Không có quyền
    ctrl --> bd : Lỗi: "Unauthorized"
    bd --> user : Hiển thị lỗi
else Có quyền
    ctrl -> inv : Cập nhật quantity\\nSet lastUpdated = now()
    activate inv
    inv -> db : UPDATE inventory\\nSET quantity=?, lastUpdated=?
    activate db
    db --> inv : OK
    deactivate db
    inv --> ctrl : Inventory đã cập nhật
    deactivate inv
    ctrl --> bd : Trả về Inventory
    deactivate ctrl
    bd --> user : Thông báo cập nhật thành công
end
deactivate bd
@enduml"""

# ====== 17. Tạo khách hàng ======
D["SEQ17_TaoKhachHang.puml"] = f"""@startuml
title Biểu đồ tuần tự: Tạo khách hàng
{SKIN}
actor "Cashier" as user
boundary "Form_KhachHang" as bd
control "Control_Customer" as ctrl
entity "Entity_Customer" as ent
entity "Entity_Branch" as branch
database "CSDL" as db

user -> bd : Chọn "Tạo khách hàng"\\n(từ màn hình POS)
activate bd
bd --> user : Hiển thị form khách hàng
user -> bd : Nhập thông tin\\n(fullName, email, phone)
bd -> ctrl : POST /api/customers
activate ctrl

ctrl -> ctrl : Lấy currentUser từ JWT
ctrl -> branch : Lấy branch từ user
activate branch
branch -> db : SELECT * FROM branches WHERE id=?
activate db
db --> branch : Branch
deactivate db
branch --> ctrl : Branch
deactivate branch

ctrl -> ent : Kiểm tra phone trùng
activate ent
ent -> db : SELECT * FROM customers\\nWHERE phone=? AND branch_id=?
activate db
db --> ent : Kết quả
deactivate db
ent --> ctrl : Kết quả
deactivate ent

alt Phone đã tồn tại trong branch
    ctrl --> bd : Lỗi: "Customer already exists"
    bd --> user : Hiển thị lỗi
else Phone chưa tồn tại
    ctrl -> ent : Tạo Customer mới\\n(fullName, email, phone, branch)
    activate ent
    ent -> db : INSERT INTO customers(...)
    activate db
    db --> ent : Customer ID
    deactivate db
    ent --> ctrl : Customer đã tạo
    deactivate ent
    ctrl --> bd : Trả về Customer
    deactivate ctrl
    bd --> user : Thông báo tạo khách hàng thành công\\nTự động gắn vào đơn hàng hiện tại
end
deactivate bd
@enduml"""

for fname, content in D.items():
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(content)
    print(f"✓ {fname}")
print(f"\nDone! {len(D)} sequence diagrams generated.")
