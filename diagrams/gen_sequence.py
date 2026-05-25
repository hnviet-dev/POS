#!/usr/bin/env python3
"""Generate PlantUML Sequence Diagrams for POS system - BCE pattern."""
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

diagrams = {}

# ====== 1. Đăng ký tài khoản ======
diagrams["SEQ01_DangKy.puml"] = f"""@startuml
title Biểu đồ tuần tự: Đăng ký tài khoản
{SKIN}
actor "Người dùng mới" as user
boundary "Form_DangKy" as bd
control "Control_DangKy" as ctrl
entity "Entity_User" as ent
database "CSDL" as db

user -> bd : Chọn Đăng ký
activate bd
bd --> user : Hiển thị form đăng ký
user -> bd : Nhập thông tin\\n(fullName, email, password, phone)
bd -> ctrl : Gửi thông tin đăng ký
activate ctrl

ctrl -> ent : findByEmail(email)
activate ent
ent -> db : SELECT * FROM users WHERE email=?
activate db
db --> ent : Kết quả truy vấn
deactivate db
ent --> ctrl : Trả kết quả
deactivate ent

alt Email đã tồn tại
    ctrl --> bd : Lỗi: "Email already exists"
    bd --> user : Hiển thị thông báo lỗi
else Email chưa tồn tại
    alt Role = ROLE_ADMIN
        ctrl --> bd : Lỗi: "Cannot register as Admin"
        bd --> user : Hiển thị thông báo lỗi
    else Role hợp lệ
        ctrl -> ctrl : Mã hóa password\\n(BCryptPasswordEncoder)
        ctrl -> ent : Tạo User mới
        activate ent
        ent -> db : INSERT INTO users(...)
        activate db
        db --> ent : Lưu thành công
        deactivate db
        ent --> ctrl : User đã tạo
        deactivate ent
        ctrl -> ctrl : Tạo JWT Token\\n(JwtProvider.generateToken)
        ctrl --> bd : Trả về {{ jwt, user }}
        deactivate ctrl
        bd --> user : Lưu JWT vào localStorage\\nĐiều hướng vào hệ thống
    end
end
deactivate bd
@enduml"""

# ====== 2. Đăng nhập ======
diagrams["SEQ02_DangNhap.puml"] = f"""@startuml
title Biểu đồ tuần tự: Đăng nhập
{SKIN}
actor "Người dùng" as user
boundary "Form_DangNhap" as bd
control "Control_DangNhap" as ctrl
entity "Entity_User" as ent
database "CSDL" as db

user -> bd : Chọn Đăng nhập
activate bd
bd --> user : Hiển thị form đăng nhập
user -> bd : Nhập email và password
bd -> ctrl : Gửi thông tin đăng nhập
activate ctrl

ctrl -> ent : loadUserByUsername(email)
activate ent
ent -> db : SELECT * FROM users WHERE email=?
activate db
db --> ent : Kết quả truy vấn
deactivate db
ent --> ctrl : Trả kết quả
deactivate ent

alt User không tồn tại
    ctrl --> bd : Lỗi: "User not found"
    bd --> user : Hiển thị thông báo lỗi
else User tồn tại
    ctrl -> ctrl : passwordEncoder.matches()\\nSo sánh password
    alt Password sai
        ctrl --> bd : Lỗi: "Invalid password"
        bd --> user : Hiển thị thông báo lỗi
    else Password đúng
        ctrl -> ctrl : Tạo JWT Token
        ctrl -> ent : Cập nhật lastLogin
        activate ent
        ent -> db : UPDATE users SET lastLogin=?
        activate db
        db --> ent : OK
        deactivate db
        ent --> ctrl : OK
        deactivate ent
        ctrl --> bd : Trả về {{ jwt, user }}
        deactivate ctrl
        bd -> bd : Kiểm tra role
        alt ROLE_ADMIN
            bd --> user : Điều hướng /super-admin
        else ROLE_STORE_ADMIN
            bd --> user : Điều hướng /store
        else ROLE_BRANCH_MANAGER
            bd --> user : Điều hướng /branch
        else ROLE_BRANCH_CASHIER
            bd --> user : Điều hướng /cashier
        end
    end
end
deactivate bd
@enduml"""

# ====== 3. Quên mật khẩu ======
diagrams["SEQ03_QuenMatKhau.puml"] = f"""@startuml
title Biểu đồ tuần tự: Quên / Đặt lại mật khẩu
{SKIN}
actor "Người dùng" as user
boundary "Form_QuenMK" as bd
control "Control_ResetPW" as ctrl
entity "Entity_Token" as tok
entity "Entity_User" as ent
database "CSDL" as db

== Giai đoạn 1: Yêu cầu reset ==
user -> bd : Chọn "Quên mật khẩu"
activate bd
bd --> user : Hiển thị form nhập email
user -> bd : Nhập email
bd -> ctrl : POST /auth/forgot-password
activate ctrl

ctrl -> ent : findByEmail(email)
activate ent
ent -> db : SELECT * FROM users WHERE email=?
activate db
db --> ent : Kết quả
deactivate db
ent --> ctrl : User
deactivate ent

alt User không tồn tại
    ctrl --> bd : Lỗi: "User not found"
    bd --> user : Hiển thị lỗi
else User tồn tại
    ctrl -> ctrl : Tạo UUID token\\n(hết hạn 5 phút)
    ctrl -> tok : Lưu PasswordResetToken
    activate tok
    tok -> db : INSERT INTO password_reset_tokens
    activate db
    db --> tok : OK
    deactivate db
    tok --> ctrl : OK
    deactivate tok
    ctrl -> ctrl : Gửi email qua Gmail SMTP\\nchứa link reset
    ctrl --> bd : Thông báo: Đã gửi email
    deactivate ctrl
    bd --> user : Hiển thị "Kiểm tra email"
end

== Giai đoạn 2: Đặt lại mật khẩu ==
user -> bd : Click link trong email
activate bd
bd --> user : Hiển thị form nhập password mới
user -> bd : Nhập password mới
bd -> ctrl : POST /auth/reset-password\\n{{token, newPassword}}
activate ctrl

ctrl -> tok : Tìm token trong DB
activate tok
tok -> db : SELECT * FROM password_reset_tokens WHERE token=?
activate db
db --> tok : Kết quả
deactivate db
tok --> ctrl : Token
deactivate tok

alt Token hết hạn hoặc không tồn tại
    ctrl -> tok : Xóa token
    activate tok
    tok -> db : DELETE FROM password_reset_tokens
    activate db
    db --> tok : OK
    deactivate db
    tok --> ctrl : OK
    deactivate tok
    ctrl --> bd : Lỗi: "Token expired"
    bd --> user : Hiển thị lỗi
else Token hợp lệ
    ctrl -> ctrl : BCrypt encode password mới
    ctrl -> ent : Cập nhật password
    activate ent
    ent -> db : UPDATE users SET password=?
    activate db
    db --> ent : OK
    deactivate db
    ent --> ctrl : OK
    deactivate ent
    ctrl -> tok : Xóa token đã dùng
    activate tok
    tok -> db : DELETE FROM password_reset_tokens
    activate db
    db --> tok : OK
    deactivate db
    tok --> ctrl : OK
    deactivate tok
    ctrl --> bd : Thành công
    deactivate ctrl
    bd --> user : Thông báo đổi mật khẩu thành công
end
deactivate bd
@enduml"""

# ====== 4. Tạo cửa hàng ======
diagrams["SEQ04_TaoCuaHang.puml"] = f"""@startuml
title Biểu đồ tuần tự: Tạo cửa hàng
{SKIN}
actor "Store Admin" as user
boundary "Form_TaoCuaHang" as bd
control "Control_Store" as ctrl
entity "Entity_Store" as ent
database "CSDL" as db

user -> bd : Chọn "Tạo cửa hàng"
activate bd
bd --> user : Hiển thị form tạo cửa hàng
user -> bd : Nhập thông tin\\n(brand, description, storeType, contact)
bd -> ctrl : POST /api/stores
activate ctrl

ctrl -> ctrl : Lấy currentUser từ JWT
ctrl -> ent : Tạo Store mới\\n(storeAdmin = currentUser)
activate ent
ent -> ent : Set status = PENDING\\nSet createdAt = now()
ent -> db : INSERT INTO stores(...)
activate db
db --> ent : Lưu thành công
deactivate db
ent --> ctrl : Store (PENDING)
deactivate ent

ctrl --> bd : Trả về Store
deactivate ctrl
bd --> user : Hiển thị thông báo:\\n"Cửa hàng đang chờ duyệt"
deactivate bd
@enduml"""

# ====== 5. Duyệt cửa hàng ======
diagrams["SEQ05_DuyetCuaHang.puml"] = f"""@startuml
title Biểu đồ tuần tự: Duyệt cửa hàng
{SKIN}
actor "Super Admin" as admin
boundary "ManHinh_DuyetStore" as bd
control "Control_Store" as ctrl
entity "Entity_Store" as ent
database "CSDL" as db

admin -> bd : Xem danh sách Store PENDING
activate bd
bd -> ctrl : GET /api/stores/pending
activate ctrl
ctrl -> ent : Tìm stores có status=PENDING
activate ent
ent -> db : SELECT * FROM stores WHERE status='PENDING'
activate db
db --> ent : Danh sách stores
deactivate db
ent --> ctrl : List<Store>
deactivate ent
ctrl --> bd : Trả danh sách
deactivate ctrl
bd --> admin : Hiển thị danh sách chờ duyệt

admin -> bd : Chọn Store cần duyệt
bd -> ctrl : PUT /api/stores/{{id}}/moderate
activate ctrl
ctrl -> ent : findById(id)
activate ent
ent -> db : SELECT * FROM stores WHERE id=?
activate db
db --> ent : Store
deactivate db
ent --> ctrl : Store
deactivate ent

alt action = APPROVE
    ctrl -> ent : Set status = ACTIVE
    activate ent
    ent -> db : UPDATE stores SET status='ACTIVE'
    activate db
    db --> ent : OK
    deactivate db
    ent --> ctrl : Store (ACTIVE)
    deactivate ent
    ctrl --> bd : Trả về Store đã duyệt
    bd --> admin : Thông báo: Đã duyệt thành công
else action = BLOCK
    ctrl -> ent : Set status = BLOCKED
    activate ent
    ent -> db : UPDATE stores SET status='BLOCKED'
    activate db
    db --> ent : OK
    deactivate db
    ent --> ctrl : Store (BLOCKED)
    deactivate ent
    ctrl --> bd : Trả về Store bị chặn
    bd --> admin : Thông báo: Đã chặn cửa hàng
end
deactivate ctrl
deactivate bd
@enduml"""

# ====== 6. Bán hàng POS ======
diagrams["SEQ06_BanHangPOS.puml"] = f"""@startuml
title Biểu đồ tuần tự: Bán hàng POS
{SKIN}
actor "Cashier" as user
boundary "ManHinh_POS" as bd
control "Control_POS" as ctrl
entity "Entity_Order" as ord
entity "Entity_Product" as prod
database "CSDL" as db

user -> bd : Mở màn hình POS
activate bd
bd -> ctrl : GET /api/products?branch=...
activate ctrl
ctrl -> prod : Lấy danh sách sản phẩm
activate prod
prod -> db : SELECT * FROM products
activate db
db --> prod : Danh sách SP
deactivate db
prod --> ctrl : List<Product>
deactivate prod
ctrl --> bd : Trả danh sách SP
deactivate ctrl
bd --> user : Hiển thị danh sách sản phẩm

loop Thêm sản phẩm vào giỏ
    user -> bd : Chọn sản phẩm + số lượng
    bd -> bd : Redux: cartSlice.addItem()\\nTính toán realtime\\n(subtotal, tax, total)
    bd --> user : Cập nhật giỏ hàng
end

user -> bd : Chọn khách hàng (tùy chọn)
user -> bd : Chọn phương thức thanh toán\\n(CASH / CARD / UPI)
user -> bd : Nhấn "Thanh toán"

bd -> ctrl : POST /api/orders
activate ctrl
ctrl -> ctrl : Lấy cashier từ JWT\\nLấy branch từ cashier
ctrl -> ord : Tạo Order mới
activate ord
ord -> ord : Set status = COMPLETED\\nSet paymentType\\nSet totalAmount
ord -> db : INSERT INTO orders(...)
activate db
db --> ord : Order ID
deactivate db

loop Lưu từng OrderItem
    ord -> db : INSERT INTO order_items(...)
    activate db
    db --> ord : OK
    deactivate db
end

ord --> ctrl : Order đã tạo
deactivate ord
ctrl --> bd : Trả về Order
deactivate ctrl
bd -> bd : Redux: clearCart()
bd --> user : Hiển thị hóa đơn thành công
deactivate bd
@enduml"""

# ====== 7. Kết thúc ca làm việc ======
diagrams["SEQ07_KetThucCa.puml"] = f"""@startuml
title Biểu đồ tuần tự: Kết thúc ca làm việc
{SKIN}
actor "Cashier" as user
boundary "ManHinh_Shift" as bd
control "Control_Shift" as ctrl
entity "Entity_ShiftReport" as shift
entity "Entity_Order" as ord
entity "Entity_Refund" as ref
database "CSDL" as db

user -> bd : Nhấn "Kết thúc ca"
activate bd
bd -> ctrl : PUT /api/shifts/{{id}}/close
activate ctrl

ctrl -> ctrl : Set shiftEnd = now()

ctrl -> ord : Lấy orders trong ca
activate ord
ord -> db : SELECT * FROM orders\\nWHERE cashier=? AND createdAt\\nBETWEEN shiftStart AND shiftEnd
activate db
db --> ord : List<Order>
deactivate db
ord --> ctrl : Danh sách đơn hàng
deactivate ord

ctrl -> ref : Lấy refunds trong ca
activate ref
ref -> db : SELECT * FROM refunds\\nWHERE cashier=? AND createdAt\\nBETWEEN shiftStart AND shiftEnd
activate db
db --> ref : List<Refund>
deactivate db
ref --> ctrl : Danh sách hoàn trả
deactivate ref

ctrl -> ctrl : Tính toán:\\ntotalSales = SUM(orders)\\ntotalRefunds = SUM(refunds)\\nnetSales = totalSales - totalRefunds\\ntotalOrders = COUNT(orders)

ctrl -> ctrl : Tính PaymentSummary\\n(nhóm theo CASH/CARD/UPI)

ctrl -> ctrl : Tính Top 5 sản phẩm\\nbán chạy nhất

ctrl -> shift : Lưu ShiftReport
activate shift
shift -> db : UPDATE shift_reports SET\\ntotalSales=?, totalRefunds=?,\\nnetSales=?, shiftEnd=?
activate db
db --> shift : OK
deactivate db
shift --> ctrl : ShiftReport
deactivate shift

ctrl --> bd : Trả về báo cáo ca
deactivate ctrl
bd --> user : Hiển thị tổng kết ca:\\n- Tổng doanh thu\\n- Tổng hoàn trả\\n- Doanh thu thuần\\n- Top 5 SP bán chạy
deactivate bd
@enduml"""

# Write all files
for fname, content in diagrams.items():
    path = os.path.join(OUT, fname)
    with open(path, "w") as f:
        f.write(content)
    print(f"✓ {fname}")

print(f"\nDone! {len(diagrams)} sequence diagrams generated.")
