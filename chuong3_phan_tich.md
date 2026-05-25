# 3.2 Phân tích hệ thống

## 3.2.1 Xác định các tác nhân Actor và chức năng (Usecase)

| STT | Tác nhân | Mã Role | Mô tả | Chức năng chính |
|-----|----------|---------|-------|----------------|
| 1 | Super Admin | ROLE_ADMIN | Quản trị viên cao nhất của toàn nền tảng | Quản lý stores, duyệt/chặn cửa hàng, quản lý gói dịch vụ, xem dashboard tổng quan |
| 2 | Store Admin | ROLE_STORE_ADMIN | Chủ sở hữu cửa hàng | Quản lý chi nhánh, sản phẩm, danh mục, nhân viên, xem analytics toàn store |
| 3 | Store Manager | ROLE_STORE_MANAGER | Quản lý cửa hàng (được ủy quyền) | Tương tự Store Admin nhưng không phải chủ sở hữu |
| 4 | Branch Manager | ROLE_BRANCH_MANAGER | Quản lý chi nhánh | Xem đơn hàng, quản lý tồn kho, xem nhân viên, xem analytics chi nhánh |
| 5 | Branch Admin | ROLE_BRANCH_ADMIN | Quản trị viên chi nhánh | Hỗ trợ Branch Manager quản lý chi nhánh |
| 6 | Cashier | ROLE_BRANCH_CASHIER | Thu ngân tại quầy | Bán hàng POS, quản lý ca, tạo hoàn trả, xem lịch sử đơn |
| 7 | Customer | ROLE_CUSTOMER | Khách hàng | Được quản lý trong hệ thống, liên kết với đơn hàng |

*Bảng 3.3 Tác nhân và chức năng*

## 3.2.2 Biểu đồ UseCase tổng quát

*(Chèn hình vẽ từ draw.io: diagrams/UC_TongQuat.drawio)*

*Hình 3.2 Biểu đồ USECASE tổng quát*

## 3.2.3 Biểu đồ UseCase chi tiết

### 3.2.3.1 Biểu đồ usecase chi tiết Xác thực hệ thống

*(Chèn hình vẽ từ draw.io: diagrams/UC_XacThuc.drawio)*

*Hình 3.3 Biểu đồ usecase chi tiết Xác thực hệ thống*

- Kịch bản usecase Đăng nhập hệ thống

| **Tên Usecase** | Đăng nhập hệ thống |
|---|---|
| **Tác nhân** | Super Admin, Store Admin, Branch Manager, Cashier |
| **Mô tả** | Người dùng nhập email và mật khẩu để truy cập hệ thống. Hệ thống xác thực bằng BCrypt, cấp JWT token và điều hướng đến giao diện phù hợp với vai trò. |
| **Tiền điều kiện** | Người dùng đã có tài khoản trong hệ thống và chưa đăng nhập |
| **Luồng sự kiện chính** | 1. Người dùng truy cập trang đăng nhập (/login)<br>2. Nhập email và mật khẩu<br>3. Nhấn nút "Đăng nhập"<br>4. Hệ thống gọi API POST /auth/login<br>5. Backend tìm User theo email trong database<br>6. So sánh mật khẩu bằng BCrypt<br>7. Tạo JWT token (HS512, 24 giờ) chứa email và role<br>8. Trả về JWT + thông tin user<br>9. Frontend lưu JWT vào localStorage<br>10. Điều hướng theo role |
| **Luồng sự kiện phụ** | 1. Email không tồn tại → "User not found"<br>2. Mật khẩu sai → "Invalid password" |

*Bảng 3.4 Đặc tả usecase Đăng nhập hệ thống*

- Kịch bản usecase Đăng ký tài khoản

| **Tên Usecase** | Đăng ký tài khoản |
|---|---|
| **Tác nhân** | Store Admin (người dùng mới) |
| **Mô tả** | Người dùng mới đăng ký tài khoản Store Admin để tạo và quản lý cửa hàng. |
| **Tiền điều kiện** | Email chưa tồn tại trong hệ thống |
| **Luồng sự kiện chính** | 1. Truy cập trang đăng ký<br>2. Nhập: Full Name, Email, Password<br>3. Nhấn nút "Đăng ký"<br>4. Hệ thống gọi API POST /auth/signup<br>5. Backend kiểm tra email trùng<br>6. Mã hóa mật khẩu bằng BCrypt<br>7. Tạo User với role = ROLE_STORE_ADMIN<br>8. Tạo JWT token<br>9. Chuyển đến trang Onboarding |
| **Luồng sự kiện phụ** | 1. Email đã tồn tại → "Email is already used" |

*Bảng 3.5 Đặc tả usecase Đăng ký tài khoản*

- Kịch bản usecase Quên mật khẩu

| **Tên Usecase** | Quên mật khẩu |
|---|---|
| **Tác nhân** | Tất cả người dùng |
| **Mô tả** | Người dùng yêu cầu đặt lại mật khẩu qua email. Hệ thống tạo token và gửi link qua Gmail SMTP. |
| **Tiền điều kiện** | Người dùng có tài khoản với email hợp lệ |
| **Luồng sự kiện chính** | 1. Nhấn "Quên mật khẩu" tại trang đăng nhập<br>2. Nhập email đã đăng ký<br>3. Hệ thống gọi API POST /auth/forgot-password<br>4. Backend tìm User theo email<br>5. Tạo token UUID, hạn 5 phút<br>6. Lưu PasswordResetToken vào database<br>7. Gửi email qua Gmail SMTP với link reset<br>8. Hiển thị "Đã gửi email đặt lại mật khẩu" |
| **Luồng sự kiện phụ** | 1. Email không tồn tại → "User not found"<br>2. Gửi email thất bại → Lỗi SMTP |

*Bảng 3.6 Đặc tả usecase Quên mật khẩu*

- Kịch bản usecase Đặt lại mật khẩu

| **Tên Usecase** | Đặt lại mật khẩu |
|---|---|
| **Tác nhân** | Tất cả người dùng |
| **Mô tả** | Người dùng click link trong email và nhập mật khẩu mới. |
| **Tiền điều kiện** | Token hợp lệ (chưa hết hạn 5 phút) |
| **Luồng sự kiện chính** | 1. Click link trong email → /reset-password?token=...<br>2. Nhập mật khẩu mới + xác nhận<br>3. Gọi API POST /auth/reset-password<br>4. Backend tìm token, kiểm tra hạn<br>5. Mã hóa mật khẩu mới bằng BCrypt<br>6. Cập nhật User.password<br>7. Xóa token khỏi database<br>8. Chuyển về trang đăng nhập |
| **Luồng sự kiện phụ** | 1. Token không tồn tại → "Invalid token"<br>2. Token hết hạn → "Token expired" |

*Bảng 3.7 Đặc tả usecase Đặt lại mật khẩu*

### 3.2.3.2 Biểu đồ usecase chi tiết Quản lý cửa hàng

*(Chèn hình vẽ từ draw.io: diagrams/UC_CuaHang.drawio)*

*Hình 3.4 Biểu đồ usecase chi tiết Quản lý cửa hàng*

- Kịch bản usecase Tạo cửa hàng mới

| **Tên Usecase** | Tạo cửa hàng mới |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Store Admin tạo cửa hàng mới qua Onboarding. Cửa hàng được tạo với status = PENDING chờ duyệt. |
| **Tiền điều kiện** | Store Admin đã đăng nhập, chưa có cửa hàng |
| **Luồng sự kiện chính** | 1. Hệ thống hiển thị form Onboarding (2 bước)<br>2. Bước 1: Nhập thông tin chủ cửa hàng<br>3. Bước 2: Nhập brand, description, storeType, contact<br>4. Nhấn "Tạo cửa hàng"<br>5. Gọi API POST /api/stores<br>6. Backend tạo Store (status = PENDING)<br>7. Liên kết Store với User<br>8. Hiển thị "Cửa hàng đang chờ duyệt" |
| **Luồng sự kiện phụ** | 1. Đã có cửa hàng → Chuyển Dashboard<br>2. Dữ liệu không hợp lệ → Lỗi validation |

*Bảng 3.8 Đặc tả usecase Tạo cửa hàng mới*

- Kịch bản usecase Duyệt cửa hàng

| **Tên Usecase** | Duyệt cửa hàng (Approve) |
|---|---|
| **Tác nhân** | Super Admin |
| **Mô tả** | Super Admin duyệt cửa hàng PENDING để cho phép hoạt động. |
| **Tiền điều kiện** | Super Admin đã đăng nhập. Có store với status = PENDING |
| **Luồng sự kiện chính** | 1. Truy cập trang Pending Requests<br>2. Hệ thống hiển thị DS store PENDING<br>3. Chọn store cần duyệt<br>4. Xem chi tiết: brand, description, contact<br>5. Nhấn "Approve"<br>6. Gọi API PUT /api/stores/{id}/moderate<br>7. Backend cập nhật status = ACTIVE<br>8. Cửa hàng hoạt động bình thường |
| **Luồng sự kiện phụ** | 1. Không có store PENDING → "No pending requests" |

*Bảng 3.9 Đặc tả usecase Duyệt cửa hàng*

- Kịch bản usecase Chặn cửa hàng

| **Tên Usecase** | Chặn cửa hàng (Block) |
|---|---|
| **Tác nhân** | Super Admin |
| **Mô tả** | Super Admin chặn hoạt động của cửa hàng vi phạm. |
| **Tiền điều kiện** | Super Admin đã đăng nhập. Cửa hàng đang ACTIVE |
| **Luồng sự kiện chính** | 1. Truy cập trang Store List<br>2. Chọn cửa hàng cần chặn<br>3. Nhấn "Block"<br>4. Gọi API PUT /api/stores/{id}/moderate (BLOCKED)<br>5. Backend cập nhật status = BLOCKED<br>6. Cửa hàng không thể hoạt động |
| **Luồng sự kiện phụ** | 1. Đã bị BLOCKED → Hiện nút "Unblock" |

*Bảng 3.10 Đặc tả usecase Chặn cửa hàng*

- Kịch bản usecase Cập nhật thông tin cửa hàng

| **Tên Usecase** | Cập nhật thông tin cửa hàng |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Store Admin cập nhật brand, description, storeType, contact. |
| **Tiền điều kiện** | Store Admin đã đăng nhập, sở hữu cửa hàng |
| **Luồng sự kiện chính** | 1. Truy cập trang Store Information<br>2. Nhấn "Edit Store"<br>3. Sửa thông tin cần thiết<br>4. Nhấn "Save"<br>5. Gọi API PUT /api/stores/{id}<br>6. Backend kiểm tra quyền sở hữu<br>7. Cập nhật database<br>8. Hiển thị thông báo thành công |
| **Luồng sự kiện phụ** | 1. Không có quyền → "Access denied" |

*Bảng 3.11 Đặc tả usecase Cập nhật thông tin cửa hàng*

### 3.2.3.3 Biểu đồ usecase chi tiết Quản lý chi nhánh

*(Chèn hình vẽ từ draw.io: diagrams/UC_ChiNhanh.drawio)*

*Hình 3.5 Biểu đồ usecase chi tiết Quản lý chi nhánh*

- Kịch bản usecase Thêm chi nhánh mới

| **Tên Usecase** | Thêm chi nhánh mới |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Tạo chi nhánh mới gồm địa chỉ, giờ hoạt động, ngày làm việc. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Cửa hàng đã ACTIVE |
| **Luồng sự kiện chính** | 1. Truy cập trang Branches<br>2. Nhấn "Add Branch"<br>3. Nhập: name, address, city, state, phone, email<br>4. Chọn openTime, closeTime, workingDays<br>5. Nhấn "Create"<br>6. Gọi API POST /api/branches<br>7. Backend tạo Branch liên kết Store<br>8. Hiển thị branch mới trong danh sách |
| **Luồng sự kiện phụ** | 1. Vượt giới hạn maxBranches → Thông báo nâng cấp<br>2. Dữ liệu không hợp lệ → Lỗi validation |

*Bảng 3.12 Đặc tả usecase Thêm chi nhánh mới*

- Kịch bản usecase Sửa thông tin chi nhánh

| **Tên Usecase** | Sửa thông tin chi nhánh |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Cập nhật thông tin chi nhánh đã tạo. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Chi nhánh tồn tại |
| **Luồng sự kiện chính** | 1. Truy cập trang Branches<br>2. Chọn chi nhánh, nhấn "Edit"<br>3. Hệ thống hiển thị form với dữ liệu hiện tại<br>4. Sửa các trường cần thiết<br>5. Nhấn "Save"<br>6. Gọi API PUT /api/branches/{id}<br>7. Cập nhật database<br>8. Thông báo thành công |
| **Luồng sự kiện phụ** | 1. Branch không tồn tại → "Branch not found" |

*Bảng 3.13 Đặc tả usecase Sửa thông tin chi nhánh*

- Kịch bản usecase Xóa chi nhánh

| **Tên Usecase** | Xóa chi nhánh |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Xóa chi nhánh không còn hoạt động. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Chi nhánh tồn tại |
| **Luồng sự kiện chính** | 1. Truy cập trang Branches<br>2. Chọn chi nhánh, nhấn "Delete"<br>3. Xác nhận "Bạn có chắc muốn xóa?"<br>4. Nhấn "Confirm"<br>5. Gọi API DELETE /api/branches/{id}<br>6. Backend xóa chi nhánh<br>7. Cập nhật danh sách |
| **Luồng sự kiện phụ** | 1. Còn nhân viên/đơn hàng → Không cho xóa |

*Bảng 3.14 Đặc tả usecase Xóa chi nhánh*

### 3.2.3.4 Biểu đồ usecase chi tiết Quản lý sản phẩm và danh mục

*(Chèn hình vẽ từ draw.io: diagrams/UC_SanPham_DanhMuc.drawio)*

*Hình 3.6 Biểu đồ usecase chi tiết Quản lý sản phẩm và danh mục*

- Kịch bản usecase Thêm sản phẩm

| **Tên Usecase** | Thêm sản phẩm |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Tạo sản phẩm mới với ảnh upload lên Cloudinary. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Có ít nhất 1 danh mục |
| **Luồng sự kiện chính** | 1. Truy cập trang Products<br>2. Nhấn "Add Product"<br>3. Nhập: name, description, price, mrpPrice<br>4. Chọn category<br>5. Upload ảnh sản phẩm<br>6. Nhấn "Create"<br>7. Frontend upload ảnh lên Cloudinary → nhận URL<br>8. Gọi API POST /api/products với imageUrl<br>9. Backend tạo Product liên kết Store<br>10. Hiển thị sản phẩm mới |
| **Luồng sự kiện phụ** | 1. Vượt giới hạn maxProducts → Nâng cấp gói<br>2. Upload ảnh thất bại → Lỗi Cloudinary |

*Bảng 3.15 Đặc tả usecase Thêm sản phẩm*

- Kịch bản usecase Sửa sản phẩm

| **Tên Usecase** | Sửa sản phẩm |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Cập nhật thông tin sản phẩm. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Sản phẩm tồn tại |
| **Luồng sự kiện chính** | 1. Chọn sản phẩm, nhấn "Edit"<br>2. Sửa thông tin cần thiết<br>3. Thay đổi ảnh nếu cần<br>4. Nhấn "Save"<br>5. Gọi API PUT /api/products/{id}<br>6. Backend cập nhật database<br>7. Thông báo thành công |
| **Luồng sự kiện phụ** | 1. Sản phẩm không tồn tại → "Product not found" |

*Bảng 3.16 Đặc tả usecase Sửa sản phẩm*

- Kịch bản usecase Xóa sản phẩm

| **Tên Usecase** | Xóa sản phẩm |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Xóa sản phẩm khỏi hệ thống. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Sản phẩm tồn tại |
| **Luồng sự kiện chính** | 1. Chọn sản phẩm, nhấn "Delete"<br>2. Xác nhận xóa<br>3. Gọi API DELETE /api/products/{id}<br>4. Backend xóa sản phẩm<br>5. Cập nhật danh sách |
| **Luồng sự kiện phụ** | 1. Sản phẩm đang trong đơn → Cảnh báo |

*Bảng 3.17 Đặc tả usecase Xóa sản phẩm*

- Kịch bản usecase Thêm danh mục

| **Tên Usecase** | Thêm danh mục |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Tạo danh mục sản phẩm mới cho cửa hàng. |
| **Tiền điều kiện** | Store Admin đã đăng nhập |
| **Luồng sự kiện chính** | 1. Truy cập trang Categories<br>2. Nhấn "Add Category"<br>3. Nhập: name<br>4. Nhấn "Create"<br>5. Gọi API POST /api/categories<br>6. Backend tạo Category liên kết Store<br>7. Hiển thị danh mục mới |
| **Luồng sự kiện phụ** | 1. Tên trùng → Thông báo lỗi |

*Bảng 3.18 Đặc tả usecase Thêm danh mục*

- Kịch bản usecase Sửa danh mục

| **Tên Usecase** | Sửa danh mục |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Cập nhật tên danh mục. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Danh mục tồn tại |
| **Luồng sự kiện chính** | 1. Chọn danh mục, nhấn "Edit"<br>2. Sửa tên<br>3. Nhấn "Save"<br>4. Gọi API PUT /api/categories/{id}<br>5. Cập nhật database |
| **Luồng sự kiện phụ** | 1. Danh mục không tồn tại → Lỗi |

*Bảng 3.19 Đặc tả usecase Sửa danh mục*

- Kịch bản usecase Xóa danh mục

| **Tên Usecase** | Xóa danh mục |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Xóa danh mục không còn sử dụng. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Danh mục tồn tại |
| **Luồng sự kiện chính** | 1. Chọn danh mục, nhấn "Delete"<br>2. Xác nhận xóa<br>3. Gọi API DELETE /api/categories/{id}<br>4. Backend xóa danh mục<br>5. Cập nhật danh sách |
| **Luồng sự kiện phụ** | 1. Còn sản phẩm thuộc danh mục → Không cho xóa |

*Bảng 3.20 Đặc tả usecase Xóa danh mục*

### 3.2.3.5 Biểu đồ usecase chi tiết Quản lý nhân viên

*(Chèn hình vẽ từ draw.io: diagrams/UC_NhanVien.drawio)*

*Hình 3.7 Biểu đồ usecase chi tiết Quản lý nhân viên*

- Kịch bản usecase Thêm nhân viên

| **Tên Usecase** | Thêm nhân viên |
|---|---|
| **Tác nhân** | Store Admin, Branch Manager |
| **Mô tả** | Tạo tài khoản nhân viên mới (Store Manager, Branch Manager, Cashier). |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Truy cập trang Employees<br>2. Nhấn "Add Employee"<br>3. Nhập: fullName, email, password, phone<br>4. Chọn role (STORE_MANAGER / BRANCH_MANAGER / BRANCH_CASHIER)<br>5. Chọn branch (nếu role cấp branch)<br>6. Nhấn "Create"<br>7. Gọi API POST /api/employees/store/{storeId} hoặc /branch/{branchId}<br>8. Backend tạo User và gán role<br>9. Hiển thị nhân viên mới |
| **Luồng sự kiện phụ** | 1. Email đã tồn tại → Thông báo lỗi<br>2. Vượt giới hạn maxUsers → Nâng cấp gói |

*Bảng 3.21 Đặc tả usecase Thêm nhân viên*

- Kịch bản usecase Sửa thông tin nhân viên

| **Tên Usecase** | Sửa thông tin nhân viên |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Cập nhật thông tin nhân viên (tên, phone, role). |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Chọn nhân viên cần sửa<br>2. Nhấn "Edit"<br>3. Sửa thông tin cần thiết<br>4. Nhấn "Save"<br>5. Gọi API PUT /api/employees/{id}<br>6. Backend cập nhật database<br>7. Thông báo thành công |
| **Luồng sự kiện phụ** | 1. Dữ liệu không hợp lệ → Lỗi validation |

*Bảng 3.22 Đặc tả usecase Sửa thông tin nhân viên*

- Kịch bản usecase Xóa nhân viên

| **Tên Usecase** | Xóa nhân viên |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Xóa tài khoản nhân viên khỏi hệ thống. |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Chọn nhân viên cần xóa<br>2. Nhấn "Delete"<br>3. Xác nhận xóa<br>4. Gọi API DELETE /api/employees/{id}<br>5. Backend xóa User<br>6. Cập nhật danh sách |
| **Luồng sự kiện phụ** | 1. Nhân viên đang có ca → Không cho xóa |

*Bảng 3.23 Đặc tả usecase Xóa nhân viên*

### 3.2.3.6 Biểu đồ usecase chi tiết Bán hàng POS

*(Chèn hình vẽ từ draw.io: diagrams/UC_BanHangPOS.drawio)*

*Hình 3.8 Biểu đồ usecase chi tiết Bán hàng POS*

- Kịch bản usecase Tạo đơn hàng POS

| **Tên Usecase** | Tạo đơn hàng POS |
|---|---|
| **Tác nhân** | Cashier |
| **Mô tả** | Thu ngân tìm sản phẩm, thêm vào giỏ, chọn phương thức thanh toán và tạo đơn hàng. |
| **Tiền điều kiện** | Cashier đã đăng nhập, đã bắt đầu ca (Start Shift) |
| **Luồng sự kiện chính** | 1. Tìm kiếm sản phẩm bằng tên<br>2. Thêm sản phẩm vào giỏ hàng (Redux)<br>3. Điều chỉnh số lượng nếu cần<br>4. Áp dụng giảm giá (nếu có)<br>5. Chọn/tạo khách hàng<br>6. Chọn phương thức thanh toán (CASH/CARD/UPI)<br>7. Nhấn "Thanh toán"<br>8. Gọi API POST /api/orders<br>9. Backend tạo Order + OrderItems + PaymentOrder<br>10. Trả về thông tin đơn hàng hoàn tất |
| **Luồng sự kiện phụ** | 1. Sản phẩm hết hàng → Thông báo<br>2. Chưa start shift → Yêu cầu bắt đầu ca |

*Bảng 3.24 Đặc tả usecase Tạo đơn hàng POS*

- Kịch bản usecase Tạm giữ đơn hàng (Hold Order)

| **Tên Usecase** | Tạm giữ đơn hàng |
|---|---|
| **Tác nhân** | Cashier |
| **Mô tả** | Lưu tạm giỏ hàng hiện tại để phục vụ khách khác, sau đó khôi phục lại. |
| **Tiền điều kiện** | Có sản phẩm trong giỏ hàng |
| **Luồng sự kiện chính** | 1. Nhấn "Hold Order"<br>2. Frontend lưu giỏ hàng vào heldOrders[] (Redux)<br>3. Xóa giỏ hàng hiện tại<br>4. Phục vụ khách mới<br>5. Nhấn "Restore" trên đơn tạm giữ<br>6. Khôi phục giỏ hàng từ heldOrders[] |
| **Luồng sự kiện phụ** | 1. Không có sản phẩm → Không cho Hold |

*Bảng 3.25 Đặc tả usecase Tạm giữ đơn hàng*

### 3.2.3.7 Biểu đồ usecase chi tiết Quản lý ca làm việc và hoàn trả

*(Chèn hình vẽ từ draw.io: diagrams/UC_CaLamViec_HoanTra.drawio)*

*Hình 3.9 Biểu đồ usecase chi tiết Quản lý ca làm việc và hoàn trả*

- Kịch bản usecase Bắt đầu ca làm việc

| **Tên Usecase** | Bắt đầu ca làm việc (Start Shift) |
|---|---|
| **Tác nhân** | Cashier |
| **Mô tả** | Cashier bắt đầu ca làm việc trước khi bán hàng. |
| **Tiền điều kiện** | Cashier đã đăng nhập, chưa có ca đang mở |
| **Luồng sự kiện chính** | 1. Nhấn "Start Shift"<br>2. Gọi API POST /api/shift-reports/start<br>3. Backend tạo ShiftReport{cashierId, branchId, shiftStart=now()}<br>4. Trả về shiftReportId<br>5. Cashier có thể bắt đầu bán hàng |
| **Luồng sự kiện phụ** | 1. Đã có ca đang mở → Thông báo |

*Bảng 3.26 Đặc tả usecase Bắt đầu ca làm việc*

- Kịch bản usecase Kết thúc ca làm việc

| **Tên Usecase** | Kết thúc ca làm việc (End Shift) |
|---|---|
| **Tác nhân** | Cashier |
| **Mô tả** | Kết thúc ca, hệ thống tự động tổng kết doanh thu, hoàn trả, top sản phẩm. |
| **Tiền điều kiện** | Có ca đang mở |
| **Luồng sự kiện chính** | 1. Nhấn "End Shift"<br>2. Gọi API PATCH /api/shift-reports/end<br>3. Backend query orders trong [shiftStart, now]<br>4. Tính totalSales, totalRefunds, netSales<br>5. Tính topSellingProducts<br>6. Lưu vào ShiftReport<br>7. Hiển thị báo cáo ca |
| **Luồng sự kiện phụ** | 1. Không có ca → Thông báo lỗi |

*Bảng 3.27 Đặc tả usecase Kết thúc ca làm việc*

- Kịch bản usecase Tạo hoàn trả

| **Tên Usecase** | Tạo hoàn trả (Refund) |
|---|---|
| **Tác nhân** | Cashier |
| **Mô tả** | Hoàn trả đơn hàng đã thanh toán cho khách hàng. |
| **Tiền điều kiện** | Có đơn hàng đã thanh toán thành công |
| **Luồng sự kiện chính** | 1. Tìm đơn hàng cần hoàn trả<br>2. Nhập lý do hoàn trả, số tiền<br>3. Chọn phương thức hoàn tiền<br>4. Nhấn "Refund"<br>5. Gọi API POST /api/refunds<br>6. Backend tạo Refund, cập nhật Order status = REFUNDED<br>7. Liên kết Refund với ShiftReport |
| **Luồng sự kiện phụ** | 1. Đơn hàng đã hoàn trả → Không cho trùng |

*Bảng 3.28 Đặc tả usecase Tạo hoàn trả*

### 3.2.3.8 Biểu đồ usecase chi tiết Quản lý tồn kho và khách hàng

*(Chèn hình vẽ từ draw.io: diagrams/UC_TonKho_KhachHang.drawio)*

*Hình 3.10 Biểu đồ usecase chi tiết Quản lý tồn kho và khách hàng*

- Kịch bản usecase Cập nhật tồn kho

| **Tên Usecase** | Cập nhật tồn kho |
|---|---|
| **Tác nhân** | Branch Manager |
| **Mô tả** | Cập nhật số lượng tồn kho sản phẩm tại chi nhánh. |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Truy cập trang Inventory<br>2. Xem danh sách tồn kho chi nhánh<br>3. Chọn sản phẩm cần cập nhật<br>4. Nhập số lượng mới<br>5. Nhấn "Update"<br>6. Gọi API PUT /api/inventories/{id}<br>7. Backend cập nhật quantity |
| **Luồng sự kiện phụ** | 1. Số lượng < 0 → Không cho cập nhật |

*Bảng 3.29 Đặc tả usecase Cập nhật tồn kho*

- Kịch bản usecase Thêm khách hàng

| **Tên Usecase** | Thêm khách hàng mới |
|---|---|
| **Tác nhân** | Cashier, Branch Manager |
| **Mô tả** | Tạo hồ sơ khách hàng mới để liên kết với đơn hàng. |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Nhấn "Add Customer"<br>2. Nhập: fullName, email, phone<br>3. Nhấn "Create"<br>4. Gọi API POST /api/customers<br>5. Backend tạo Customer<br>6. Hiển thị khách hàng mới |
| **Luồng sự kiện phụ** | 1. Email/phone trùng → Thông báo lỗi |

*Bảng 3.30 Đặc tả usecase Thêm khách hàng*

- Kịch bản usecase Sửa thông tin khách hàng

| **Tên Usecase** | Sửa thông tin khách hàng |
|---|---|
| **Tác nhân** | Branch Manager |
| **Mô tả** | Cập nhật thông tin khách hàng. |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Chọn khách hàng cần sửa<br>2. Nhấn "Edit"<br>3. Sửa thông tin cần thiết<br>4. Nhấn "Save"<br>5. Gọi API PUT /api/customers/{id}<br>6. Cập nhật database |
| **Luồng sự kiện phụ** | 1. Dữ liệu không hợp lệ → Lỗi |

*Bảng 3.31 Đặc tả usecase Sửa thông tin khách hàng*

### 3.2.3.9 Biểu đồ usecase chi tiết Subscription và thanh toán

*(Chèn hình vẽ từ draw.io: diagrams/UC_Subscription.drawio)*

*Hình 3.11 Biểu đồ usecase chi tiết Subscription và thanh toán*

- Kịch bản usecase Đăng ký gói dịch vụ

| **Tên Usecase** | Đăng ký gói dịch vụ (Subscribe) |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Store Admin chọn và đăng ký gói dịch vụ, thanh toán qua Payment Gateway. |
| **Tiền điều kiện** | Store Admin đã đăng nhập. Cửa hàng đã ACTIVE |
| **Luồng sự kiện chính** | 1. Truy cập trang Subscription<br>2. Xem danh sách gói dịch vụ<br>3. Chọn gói phù hợp<br>4. Nhấn "Subscribe"<br>5. Gọi API POST /api/subscriptions/subscribe<br>6. Backend tạo Subscription (TRIAL)<br>7. Tạo PaymentOrder → Gọi Razorpay API<br>8. Redirect đến trang thanh toán<br>9. Thanh toán thành công → Kích hoạt gói |
| **Luồng sự kiện phụ** | 1. Thanh toán thất bại → Giữ TRIAL<br>2. Đã có gói → Hiện nút "Upgrade" |

*Bảng 3.32 Đặc tả usecase Đăng ký gói dịch vụ*

- Kịch bản usecase Quản lý gói Subscription (Super Admin)

| **Tên Usecase** | Quản lý gói Subscription |
|---|---|
| **Tác nhân** | Super Admin |
| **Mô tả** | Super Admin CRUD các gói dịch vụ (plan) trên nền tảng. |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Truy cập trang Subscription Plans<br>2. Thêm/Sửa/Xóa gói: name, price, billingCycle<br>3. Cấu hình: maxBranches, maxUsers, maxProducts<br>4. Thiết lập featureFlags<br>5. Nhấn "Save"<br>6. Gọi API tương ứng (POST/PUT/DELETE)<br>7. Cập nhật database |
| **Luồng sự kiện phụ** | 1. Gói đang có store sử dụng → Không cho xóa |

*Bảng 3.33 Đặc tả usecase Quản lý gói Subscription*

### 3.2.3.10 Biểu đồ usecase chi tiết Báo cáo và Dashboard

*(Chèn hình vẽ từ draw.io: diagrams/UC_BaoCao_Dashboard.drawio)*

*Hình 3.12 Biểu đồ usecase chi tiết Báo cáo và Dashboard*

- Kịch bản usecase Xem Dashboard tổng quan

| **Tên Usecase** | Xem Dashboard tổng quan |
|---|---|
| **Tác nhân** | Super Admin |
| **Mô tả** | Xem thống kê tổng quan toàn hệ thống: số store, trạng thái, doanh thu. |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Truy cập Dashboard<br>2. Gọi API GET /api/super-admin/dashboard/summary<br>3. Hiển thị: totalStores, activeStores, pendingStores, blockedStores<br>4. Hiển thị biểu đồ thống kê |
| **Luồng sự kiện phụ** | 1. Không có dữ liệu → Hiển thị trống |

*Bảng 3.34 Đặc tả usecase Xem Dashboard tổng quan*

- Kịch bản usecase Xem Analytics cửa hàng

| **Tên Usecase** | Xem Analytics cửa hàng |
|---|---|
| **Tác nhân** | Store Admin |
| **Mô tả** | Xem doanh thu theo thời gian, chi nhánh, danh mục. |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Truy cập Dashboard Store<br>2. Xem doanh thu theo tháng (biểu đồ line)<br>3. Xem doanh thu theo chi nhánh (biểu đồ bar)<br>4. Xem doanh thu theo danh mục (biểu đồ pie)<br>5. Xem cảnh báo hệ thống (hết hàng, refund cao) |
| **Luồng sự kiện phụ** | 1. Chưa có đơn hàng → Hiển thị "No data" |

*Bảng 3.35 Đặc tả usecase Xem Analytics cửa hàng*

- Kịch bản usecase Xem Analytics chi nhánh

| **Tên Usecase** | Xem Analytics chi nhánh |
|---|---|
| **Tác nhân** | Branch Manager |
| **Mô tả** | Xem doanh thu, top sản phẩm, hiệu suất thu ngân tại chi nhánh. |
| **Tiền điều kiện** | Tác nhân đã đăng nhập vào hệ thống |
| **Luồng sự kiện chính** | 1. Truy cập Dashboard Branch<br>2. Xem doanh thu hàng ngày (biểu đồ line)<br>3. Xem top sản phẩm bán chạy (biểu đồ bar)<br>4. Xem hiệu suất thu ngân (bảng xếp hạng)<br>5. Xem breakdown thanh toán (CASH/CARD/UPI) |
| **Luồng sự kiện phụ** | 1. Chưa có dữ liệu → Hiển thị trống |

*Bảng 3.36 Đặc tả usecase Xem Analytics chi nhánh*
