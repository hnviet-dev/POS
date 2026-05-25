# CHƯƠNG 4. THIẾT KẾ HỆ THỐNG

## 4.1 Thiết kế, xây dựng cơ sở dữ liệu

Để có một hệ thống đạt yêu cầu thì không thể bỏ qua việc thiết kế cơ sở dữ liệu. Thiết kế thế nào cho hợp lý, cho đúng yêu cầu của hệ thống. Mục này sẽ đi sâu vào việc rạch ra một hệ thống cơ sở dữ liệu phục vụ cho thiết kế.

### 4.1.1 Danh sách các bảng dữ liệu

Hệ thống Zosh POS sử dụng cơ sở dữ liệu MySQL, được ánh xạ tự động từ các Entity Class thông qua JPA/Hibernate. Tổng cộng có **20 bảng dữ liệu** được phân thành 5 nhóm chức năng.

| STT | Tên bảng | Mô tả | Nhóm |
|-----|----------|-------|------|
| 1 | users | Lưu thông tin người dùng (admin, chủ cửa hàng, thu ngân, quản lý) | Người dùng |
| 2 | password_reset_tokens | Lưu token đặt lại mật khẩu | Người dùng |
| 3 | stores | Lưu thông tin cửa hàng | Tổ chức |
| 4 | branches | Lưu thông tin chi nhánh | Tổ chức |
| 5 | branch_working_days | Lưu ngày làm việc của chi nhánh | Tổ chức |
| 6 | products | Lưu thông tin sản phẩm | Sản phẩm |
| 7 | categories | Lưu danh mục sản phẩm | Sản phẩm |
| 8 | inventories | Lưu tồn kho sản phẩm theo chi nhánh | Sản phẩm |
| 9 | orders | Lưu đơn hàng bán ra | Đơn hàng |
| 10 | order_items | Lưu chi tiết từng mặt hàng trong đơn | Đơn hàng |
| 11 | customer | Lưu thông tin khách hàng | Đơn hàng |
| 12 | shift_report | Lưu báo cáo ca làm việc | Ca & Hoàn trả |
| 13 | refund | Lưu giao dịch hoàn trả | Ca & Hoàn trả |
| 14 | shift_report_top_selling_products | Bảng trung gian: sản phẩm bán chạy trong ca | Ca & Hoàn trả |
| 15 | shift_report_recent_orders | Bảng trung gian: đơn hàng gần đây trong ca | Ca & Hoàn trả |
| 16 | subscriptions | Lưu đăng ký gói dịch vụ của cửa hàng | Thanh toán |
| 17 | subscription_plans | Lưu các gói dịch vụ hệ thống | Thanh toán |
| 18 | subscription_plan_extra_features | Lưu tính năng bổ sung của gói | Thanh toán |
| 19 | payment | Lưu giao dịch thanh toán subscription | Thanh toán |
| 20 | payment_order | Lưu lệnh thanh toán qua Payment Gateway | Thanh toán |

*Bảng 4.1 Danh sách các bảng dữ liệu*

### 4.1.2 Chi tiết các bảng dữ liệu

#### 4.1.2.1 Bảng users

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | full_name | VARCHAR(255) | NOT NULL | Họ tên người dùng |
| 3 | email | VARCHAR(255) | NOT NULL, UNIQUE | Email đăng nhập |
| 4 | password | VARCHAR(255) | | Mật khẩu đã mã hóa BCrypt |
| 5 | phone | VARCHAR(255) | | Số điện thoại |
| 6 | role | INT | NOT NULL | Vai trò (enum UserRole: 0-6) |
| 7 | store_id | BIGINT | FK → stores(id) | Cửa hàng thuộc về |
| 8 | branch_id | BIGINT | FK → branches(id) | Chi nhánh thuộc về |
| 9 | verified | BIT(1) | NOT NULL, DEFAULT 0 | Trạng thái xác minh |
| 10 | last_login | DATETIME(6) | | Thời gian đăng nhập lần cuối |
| 11 | created_at | DATETIME(6) | NOT NULL | Ngày tạo |
| 12 | updated_at | DATETIME(6) | NOT NULL | Ngày cập nhật |

*Bảng 4.2 Chi tiết bảng users*

#### 4.1.2.2 Bảng password_reset_tokens

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | token | VARCHAR(255) | NOT NULL, UNIQUE | Token UUID |
| 3 | user_id | BIGINT | FK → users(id), NOT NULL | Người dùng sở hữu |
| 4 | expiry_date | DATETIME(6) | NOT NULL | Thời gian hết hạn |

*Bảng 4.3 Chi tiết bảng password_reset_tokens*

#### 4.1.2.3 Bảng stores

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | brand | VARCHAR(255) | NOT NULL | Tên thương hiệu |
| 3 | description | VARCHAR(255) | | Mô tả cửa hàng |
| 4 | store_type | VARCHAR(255) | | Loại cửa hàng |
| 5 | status | INT | | Trạng thái (enum: PENDING, ACTIVE, BLOCKED) |
| 6 | store_admin_id | BIGINT | FK → users(id), UNIQUE | Chủ cửa hàng |
| 7 | address | VARCHAR(255) | | Địa chỉ (embedded StoreContact) |
| 8 | phone | VARCHAR(255) | | Số điện thoại liên hệ |
| 9 | email | VARCHAR(255) | | Email liên hệ |
| 10 | created_at | DATETIME(6) | | Ngày tạo |
| 11 | updated_at | DATETIME(6) | | Ngày cập nhật |

*Bảng 4.4 Chi tiết bảng stores*

#### 4.1.2.4 Bảng branches

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | name | VARCHAR(255) | | Tên chi nhánh |
| 3 | address | VARCHAR(255) | | Địa chỉ |
| 4 | phone | VARCHAR(255) | | Số điện thoại |
| 5 | email | VARCHAR(255) | | Email |
| 6 | open_time | TIME | | Giờ mở cửa |
| 7 | close_time | TIME | | Giờ đóng cửa |
| 8 | store_id | BIGINT | FK → stores(id) | Cửa hàng sở hữu |
| 9 | manager_id | BIGINT | FK → users(id), UNIQUE | Quản lý chi nhánh |
| 10 | created_at | DATETIME(6) | | Ngày tạo |
| 11 | updated_at | DATETIME(6) | | Ngày cập nhật |

*Bảng 4.5 Chi tiết bảng branches*

#### 4.1.2.5 Bảng branch_working_days

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | branch_id | BIGINT | FK → branches(id), NOT NULL | Chi nhánh |
| 2 | working_days | VARCHAR(255) | | Ngày làm việc (MONDAY, TUESDAY...) |

*Bảng 4.6 Chi tiết bảng branch_working_days*

#### 4.1.2.6 Bảng products

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | name | VARCHAR(255) | NOT NULL | Tên sản phẩm |
| 3 | sku | VARCHAR(255) | NOT NULL, UNIQUE | Mã SKU |
| 4 | description | VARCHAR(255) | | Mô tả sản phẩm |
| 5 | mrp | DOUBLE | NOT NULL | Giá niêm yết |
| 6 | selling_price | DOUBLE | NOT NULL | Giá bán thực tế |
| 7 | brand | VARCHAR(255) | | Thương hiệu |
| 8 | image | VARCHAR(255) | | URL ảnh sản phẩm |
| 9 | category_id | BIGINT | FK → categories(id) | Danh mục |
| 10 | store_id | BIGINT | FK → stores(id), NOT NULL | Cửa hàng sở hữu |
| 11 | created_at | DATETIME(6) | | Ngày tạo |
| 12 | updated_at | DATETIME(6) | | Ngày cập nhật |

*Bảng 4.7 Chi tiết bảng products*

#### 4.1.2.7 Bảng categories

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | name | VARCHAR(255) | | Tên danh mục |
| 3 | store_id | BIGINT | FK → stores(id) | Cửa hàng sở hữu |

*Bảng 4.8 Chi tiết bảng categories*

#### 4.1.2.8 Bảng inventories

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | branch_id | BIGINT | FK → branches(id), NOT NULL | Chi nhánh |
| 3 | product_id | BIGINT | FK → products(id), NOT NULL | Sản phẩm |
| 4 | quantity | INT | NOT NULL | Số lượng tồn kho |
| 5 | last_updated | DATETIME(6) | | Thời gian cập nhật cuối |

*Bảng 4.9 Chi tiết bảng inventories*

#### 4.1.2.9 Bảng orders

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | total_amount | DOUBLE | | Tổng tiền đơn hàng |
| 3 | payment_type | INT | | Phương thức thanh toán (CASH/CARD/UPI) |
| 4 | status | INT | | Trạng thái (COMPLETED/REFUNDED/CANCELLED) |
| 5 | branch_id | BIGINT | FK → branches(id) | Chi nhánh bán |
| 6 | cashier_id | BIGINT | FK → users(id) | Thu ngân thực hiện |
| 7 | customer_id | BIGINT | FK → customer(id) | Khách hàng mua |
| 8 | created_at | DATETIME(6) | | Thời gian tạo đơn |

*Bảng 4.10 Chi tiết bảng orders*

#### 4.1.2.10 Bảng order_items

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | quantity | INT | | Số lượng mua |
| 3 | price | DOUBLE | | Đơn giá tại thời điểm mua |
| 4 | product_id | BIGINT | FK → products(id) | Sản phẩm |
| 5 | order_id | BIGINT | FK → orders(id) | Đơn hàng chứa |

*Bảng 4.11 Chi tiết bảng order_items*

#### 4.1.2.11 Bảng customer

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | full_name | VARCHAR(255) | NOT NULL | Họ tên khách hàng |
| 3 | email | VARCHAR(255) | | Email |
| 4 | phone | VARCHAR(255) | | Số điện thoại |
| 5 | created_at | DATETIME(6) | NOT NULL | Ngày tạo |
| 6 | updated_at | DATETIME(6) | NOT NULL | Ngày cập nhật |

*Bảng 4.12 Chi tiết bảng customer*

#### 4.1.2.12 Bảng shift_report

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | shift_start | DATETIME(6) | | Thời gian bắt đầu ca |
| 3 | shift_end | DATETIME(6) | | Thời gian kết thúc ca |
| 4 | total_sales | DOUBLE | | Tổng doanh thu |
| 5 | total_refunds | DOUBLE | | Tổng hoàn trả |
| 6 | net_sales | DOUBLE | | Doanh thu ròng |
| 7 | total_orders | INT | | Tổng số đơn hàng |
| 8 | cashier_id | BIGINT | FK → users(id) | Thu ngân |
| 9 | branch_id | BIGINT | FK → branches(id) | Chi nhánh |

*Bảng 4.13 Chi tiết bảng shift_report*

#### 4.1.2.13 Bảng refund

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | order_id | BIGINT | FK → orders(id) | Đơn hàng hoàn trả |
| 3 | reason | VARCHAR(255) | | Lý do hoàn trả |
| 4 | amount | DOUBLE | | Số tiền hoàn |
| 5 | shift_report_id | BIGINT | FK → shift_report(id) | Ca làm việc |
| 6 | cashier_id | BIGINT | FK → users(id) | Thu ngân thực hiện |
| 7 | branch_id | BIGINT | FK → branches(id) | Chi nhánh |
| 8 | payment_type | INT | | Phương thức hoàn (CASH/CARD/UPI) |
| 9 | created_at | DATETIME(6) | | Thời gian tạo |

*Bảng 4.14 Chi tiết bảng refund*

#### 4.1.2.14 Bảng shift_report_top_selling_products

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | shift_report_id | BIGINT | FK → shift_report(id) | Ca làm việc |
| 2 | top_selling_products_id | BIGINT | FK → products(id) | Sản phẩm bán chạy |

*Bảng 4.15 Chi tiết bảng shift_report_top_selling_products*

#### 4.1.2.15 Bảng shift_report_recent_orders

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | shift_report_id | BIGINT | FK → shift_report(id) | Ca làm việc |
| 2 | recent_orders_id | BIGINT | FK → orders(id) | Đơn hàng gần đây |

*Bảng 4.16 Chi tiết bảng shift_report_recent_orders*

#### 4.1.2.16 Bảng subscriptions

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | store_id | BIGINT | FK → stores(id), NOT NULL | Cửa hàng đăng ký |
| 3 | plan_id | BIGINT | FK → subscription_plans(id), NOT NULL | Gói dịch vụ |
| 4 | start_date | DATE | NOT NULL | Ngày bắt đầu |
| 5 | end_date | DATE | NOT NULL | Ngày kết thúc |
| 6 | status | VARCHAR(20) | | Trạng thái (TRIAL/ACTIVE/EXPIRED/CANCELLED) |
| 7 | payment_gateway | VARCHAR(20) | | Cổng thanh toán (RAZORPAY/STRIPE) |
| 8 | transaction_id | VARCHAR(255) | | Mã giao dịch |
| 9 | payment_status | INT | NOT NULL | Trạng thái thanh toán (PENDING/SUCCESS/FAILED) |
| 10 | created_at | DATETIME(6) | | Ngày tạo |
| 11 | updated_at | DATETIME(6) | | Ngày cập nhật |

*Bảng 4.17 Chi tiết bảng subscriptions*

#### 4.1.2.17 Bảng subscription_plans

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | name | VARCHAR(255) | NOT NULL | Tên gói (Starter, Pro...) |
| 3 | description | VARCHAR(255) | NOT NULL | Mô tả gói |
| 4 | price | DOUBLE | NOT NULL | Giá gói |
| 5 | billing_cycle | INT | NOT NULL | Chu kỳ (MONTHLY/YEARLY) |
| 6 | max_branches | INT | NOT NULL | Số chi nhánh tối đa |
| 7 | max_users | INT | NOT NULL | Số nhân viên tối đa |
| 8 | max_products | INT | NOT NULL | Số sản phẩm tối đa |
| 9 | enable_advanced_reports | BIT(1) | | Bật báo cáo nâng cao |
| 10 | enable_inventory | BIT(1) | | Bật quản lý tồn kho |
| 11 | enable_integrations | BIT(1) | | Bật tích hợp bên ngoài |
| 12 | enable_ecommerce | BIT(1) | | Bật bán hàng online |
| 13 | enable_invoice_branding | BIT(1) | | Bật tùy chỉnh hóa đơn |
| 14 | priority_support | BIT(1) | | Hỗ trợ ưu tiên |
| 15 | enable_multi_location | BIT(1) | | Bật đa chi nhánh |
| 16 | created_at | DATETIME(6) | | Ngày tạo |
| 17 | updated_at | DATETIME(6) | | Ngày cập nhật |

*Bảng 4.18 Chi tiết bảng subscription_plans*

#### 4.1.2.18 Bảng subscription_plan_extra_features

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | subscription_plan_id | BIGINT | FK → subscription_plans(id) | Gói dịch vụ |
| 2 | extra_features | VARCHAR(255) | | Tính năng bổ sung |

*Bảng 4.19 Chi tiết bảng subscription_plan_extra_features*

#### 4.1.2.19 Bảng payment

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | user_id | BIGINT | FK → stores(id), NOT NULL | Cửa hàng thanh toán |
| 3 | subscription_id | BIGINT | FK → subscriptions(id), UNIQUE | Subscription liên kết |
| 4 | amount | DOUBLE | | Số tiền thanh toán |
| 5 | provider | INT | | Cổng thanh toán (RAZORPAY/STRIPE) |
| 6 | provider_payment_id | VARCHAR(255) | | Mã từ nhà cung cấp |
| 7 | transaction_id | VARCHAR(255) | | Mã giao dịch |
| 8 | method | VARCHAR(255) | | Phương thức (CARD/UPI/NETBANKING) |
| 9 | status | VARCHAR(20) | | Trạng thái (PENDING/SUCCESS/FAILED) |
| 10 | failure_reason | VARCHAR(255) | | Lý do thất bại |
| 11 | paid_at | DATETIME(6) | | Thời gian thanh toán |
| 12 | refund_id | VARCHAR(255) | | Mã hoàn tiền |
| 13 | created_at | DATETIME(6) | | Ngày tạo |
| 14 | updated_at | DATETIME(6) | | Ngày cập nhật |

*Bảng 4.20 Chi tiết bảng payment*

#### 4.1.2.20 Bảng payment_order

| STT | Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|---------|--------------|-----------|-------|
| 1 | id | BIGINT | PK, AUTO_INCREMENT | Khóa chính |
| 2 | amount | DOUBLE | | Số tiền |
| 3 | status | INT | DEFAULT 0 | Trạng thái (PENDING/SUCCESS/FAILED) |
| 4 | payment_link_id | VARCHAR(255) | | Link thanh toán từ Gateway |
| 5 | user_id | BIGINT | FK → users(id) | Người thanh toán |
| 6 | plan_id | BIGINT | NOT NULL | ID gói dịch vụ |

*Bảng 4.21 Chi tiết bảng payment_order*

### 4.1.3 Mối quan hệ giữa các bảng

| STT | Bảng nguồn | Bảng đích | Loại quan hệ | Khóa ngoại | Mô tả |
|-----|-----------|----------|--------------|-----------|-------|
| 1 | users | stores | N:1 | store_id | Nhân viên thuộc cửa hàng |
| 2 | users | branches | N:1 | branch_id | Nhân viên thuộc chi nhánh |
| 3 | stores | users | 1:1 | store_admin_id | Chủ cửa hàng |
| 4 | branches | stores | N:1 | store_id | Chi nhánh thuộc cửa hàng |
| 5 | branches | users | 1:1 | manager_id | Quản lý chi nhánh |
| 6 | products | categories | N:1 | category_id | Sản phẩm thuộc danh mục |
| 7 | products | stores | N:1 | store_id | Sản phẩm thuộc cửa hàng |
| 8 | categories | stores | N:1 | store_id | Danh mục thuộc cửa hàng |
| 9 | inventories | branches | N:1 | branch_id | Tồn kho tại chi nhánh |
| 10 | inventories | products | N:1 | product_id | Tồn kho sản phẩm |
| 11 | orders | branches | N:1 | branch_id | Đơn tại chi nhánh |
| 12 | orders | users | N:1 | cashier_id | Thu ngân tạo đơn |
| 13 | orders | customer | N:1 | customer_id | Khách hàng mua |
| 14 | order_items | orders | N:1 | order_id | Chi tiết thuộc đơn |
| 15 | order_items | products | N:1 | product_id | Mặt hàng trong đơn |
| 16 | shift_report | users | N:1 | cashier_id | Ca của thu ngân |
| 17 | shift_report | branches | N:1 | branch_id | Ca tại chi nhánh |
| 18 | refund | orders | N:1 | order_id | Hoàn trả đơn hàng |
| 19 | refund | shift_report | N:1 | shift_report_id | Hoàn trả trong ca |
| 20 | refund | users | N:1 | cashier_id | Thu ngân hoàn trả |
| 21 | refund | branches | N:1 | branch_id | Hoàn trả tại chi nhánh |
| 22 | subscriptions | stores | N:1 | store_id | Đăng ký của cửa hàng |
| 23 | subscriptions | subscription_plans | N:1 | plan_id | Gói đăng ký |
| 24 | payment | stores | N:1 | user_id | Thanh toán của cửa hàng |
| 25 | payment | subscriptions | 1:1 | subscription_id | Thanh toán cho subscription |
| 26 | payment_order | users | N:1 | user_id | Người tạo lệnh |
| 27 | password_reset_tokens | users | N:1 | user_id | Token của người dùng |

*Bảng 4.22 Mối quan hệ giữa các bảng*

### 4.1.4 Biểu đồ cơ sở dữ liệu (ERD)

*(Chèn hình vẽ từ draw.io hoặc MySQL Workbench)*

*Hình 4.1 Biểu đồ quan hệ thực thể (ERD)*

## 4.2 Thiết kế RESTful API

Hệ thống Zosh POS được thiết kế theo kiến trúc RESTful, sử dụng Spring Boot làm backend. Tất cả API được bảo vệ bằng JWT Authentication (trừ các endpoint công khai). Dưới đây là danh sách đầy đủ các nhóm API.

### 4.2.1 Danh sách các Controller

| STT | Controller | Base URL | Mô tả |
|-----|-----------|----------|-------|
| 1 | AuthController | /auth | Xác thực: đăng ký, đăng nhập, quên mật khẩu |
| 2 | StoreController | /api/stores | CRUD cửa hàng, duyệt cửa hàng |
| 3 | BranchController | /api/branches | CRUD chi nhánh |
| 4 | ProductController | /api/products | CRUD sản phẩm |
| 5 | CategoryController | /api/categories | CRUD danh mục sản phẩm |
| 6 | EmployeeController | /api/employees | CRUD nhân viên (thu ngân, quản lý) |
| 7 | OrderController | /api/orders | Tạo đơn, xem đơn hàng |
| 8 | CustomerController | /api/customers | CRUD khách hàng |
| 9 | InventoryController | /api/inventories | Cập nhật và truy vấn tồn kho |
| 10 | ShiftReportController | /api/shift-reports | Bắt đầu/kết thúc ca, xem báo cáo ca |
| 11 | RefundController | /api/refunds | Tạo và xem hoàn trả |
| 12 | SubscriptionController | /api/subscriptions | Đăng ký, nâng cấp, hủy gói dịch vụ |
| 13 | SubscriptionPlanController | /api/super-admin/subscription-plans | Quản lý gói dịch vụ (Super Admin) |
| 14 | PaymentController | /api/payments | Xử lý thanh toán qua Razorpay/Stripe |
| 15 | StoreAnalyticsController | /api/store/analytics | Thống kê & Dashboard chủ cửa hàng |
| 16 | BranchAnalyticsController | /api/branch-analytics | Thống kê theo chi nhánh |
| 17 | AdminDashboardController | /api/super-admin | Dashboard quản trị hệ thống |
| 18 | UserController | /api/users | Xem profile, quản lý tài khoản |

*Bảng 4.23 Danh sách các Controller*

### 4.2.2 Chi tiết API theo nhóm chức năng

#### A. Nhóm Xác thực (AuthController)

| Phương thức | URL | Mô tả | Đầu vào | Đầu ra |
|-------------|-----|-------|---------|--------|
| POST | /auth/signup | Đăng ký tài khoản | fullName, email, password, phone, role | JWT token + User |
| POST | /auth/login | Đăng nhập | email, password | JWT token + User |
| POST | /auth/forgot-password | Yêu cầu đặt lại mật khẩu | email | Thông báo gửi email |
| POST | /auth/verify-forgot-password-otp | Xác thực OTP | email, otp | Token đặt lại |
| POST | /auth/reset-password | Đặt lại mật khẩu | token, newPassword | Thành công |

*Bảng 4.24 API nhóm Xác thực*

#### B. Nhóm Quản lý Cửa hàng (StoreController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/stores/create | Tạo cửa hàng mới |
| GET | /api/stores/{id} | Lấy thông tin cửa hàng |
| PUT | /api/stores/{id} | Cập nhật cửa hàng |
| PATCH | /api/stores/{storeId}/moderate | Duyệt/Chặn cửa hàng (Admin) |

*Bảng 4.25 API nhóm Cửa hàng*

#### C. Nhóm Chi nhánh (BranchController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/branches | Tạo chi nhánh |
| GET | /api/branches/store/{storeId} | Danh sách chi nhánh theo cửa hàng |
| PUT | /api/branches/{id} | Cập nhật chi nhánh |
| DELETE | /api/branches/{id} | Xóa chi nhánh |

*Bảng 4.26 API nhóm Chi nhánh*

#### D. Nhóm Sản phẩm (ProductController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/products | Tạo sản phẩm |
| GET | /api/products/store/{storeId} | Danh sách sản phẩm theo cửa hàng |
| GET | /api/products/store/{storeId}/search | Tìm kiếm sản phẩm |
| PUT | /api/products/{id} | Cập nhật sản phẩm |
| DELETE | /api/products/{id} | Xóa sản phẩm |

*Bảng 4.27 API nhóm Sản phẩm*

#### E. Nhóm Danh mục (CategoryController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/categories | Tạo danh mục |
| GET | /api/categories/store/{storeId} | Danh sách danh mục theo cửa hàng |
| PUT | /api/categories/{id} | Cập nhật danh mục |
| DELETE | /api/categories/{id} | Xóa danh mục |

*Bảng 4.28 API nhóm Danh mục*

#### F. Nhóm Nhân viên (EmployeeController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/employees/add/employee | Thêm nhân viên mới |
| GET | /api/employees/{storeId}/employee/list | Danh sách nhân viên |
| PUT | /api/employees/{employeeId} | Cập nhật nhân viên |
| DELETE | /api/employees/{employeeId} | Xóa nhân viên |

*Bảng 4.29 API nhóm Nhân viên*

#### G. Nhóm Đơn hàng (OrderController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/orders | Tạo đơn hàng mới (POS) |
| GET | /api/orders/branch/{branchId} | Đơn hàng theo chi nhánh |
| GET | /api/orders/cashier/{cashierId} | Đơn hàng theo thu ngân |
| GET | /api/orders/recent/{branchId} | Đơn hàng gần đây |
| GET | /api/orders/today/branch/{branchId} | Đơn hàng hôm nay |

*Bảng 4.30 API nhóm Đơn hàng*

#### H. Nhóm Khách hàng (CustomerController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/customers | Tạo khách hàng |
| GET | /api/customers/store/{storeId} | Danh sách khách hàng |
| PUT | /api/customers/{id} | Cập nhật khách hàng |

*Bảng 4.31 API nhóm Khách hàng*

#### I. Nhóm Tồn kho (InventoryController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/inventories | Tạo/cập nhật tồn kho |
| GET | /api/inventories/branch/{branchId} | Tồn kho theo chi nhánh |
| GET | /api/inventories/product/{productId} | Tồn kho theo sản phẩm |
| PUT | /api/inventories/{id} | Cập nhật số lượng tồn kho |

*Bảng 4.32 API nhóm Tồn kho*

#### J. Nhóm Ca làm việc (ShiftReportController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/shift-reports/start | Bắt đầu ca mới |
| PATCH | /api/shift-reports/end | Kết thúc ca (tính tổng tự động) |
| GET | /api/shift-reports/current | Ca đang mở hiện tại |
| GET | /api/shift-reports/branch/{branchId} | Lịch sử ca theo chi nhánh |
| GET | /api/shift-reports/cashier/{cashierId} | Lịch sử ca theo thu ngân |
| GET | /api/shift-reports/cashier/{cashierId}/by-date | Ca theo ngày |
| GET | /api/shift-reports/cashier/{cashierId}/range | Ca theo khoảng thời gian |

*Bảng 4.33 API nhóm Ca làm việc*

#### K. Nhóm Hoàn trả (RefundController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/refunds | Tạo hoàn trả |
| GET | /api/refunds/shift/{shiftReportId} | Hoàn trả theo ca |
| GET | /api/refunds/branch/{branchId} | Hoàn trả theo chi nhánh |
| GET | /api/refunds/customer/{customerId} | Hoàn trả theo khách hàng |

*Bảng 4.34 API nhóm Hoàn trả*

#### L. Nhóm Subscription (SubscriptionController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/subscriptions/subscribe | Đăng ký gói dịch vụ |
| POST | /api/subscriptions/upgrade | Nâng cấp gói |
| GET | /api/subscriptions/store/{storeId} | Subscription của cửa hàng |
| PATCH | /api/subscriptions/{subscriptionId}/cancel | Hủy subscription |
| PATCH | /api/subscriptions/{subscriptionId}/activate | Kích hoạt subscription |

*Bảng 4.35 API nhóm Subscription*

#### M. Nhóm Thanh toán (PaymentController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| POST | /api/payments/proceed | Tạo Payment Link (Razorpay/Stripe) |
| GET | /api/payments/{subscriptionId}/payment-status | Kiểm tra trạng thái |

*Bảng 4.36 API nhóm Thanh toán*

#### N. Nhóm Thống kê (StoreAnalyticsController + BranchAnalyticsController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| GET | /api/store/analytics/{storeAdminId}/overview | Tổng quan cửa hàng |
| GET | /api/store/analytics/{storeAdminId}/sales-trends | Xu hướng doanh số |
| GET | /api/store/analytics/{storeAdminId}/sales/daily | Doanh số theo ngày |
| GET | /api/store/analytics/{storeAdminId}/sales/monthly | Doanh số theo tháng |
| GET | /api/store/analytics/{storeAdminId}/sales/branch | Doanh số theo chi nhánh |
| GET | /api/store/analytics/{storeAdminId}/sales/category | Doanh số theo danh mục |
| GET | /api/store/analytics/{storeAdminId}/sales/payment-method | Doanh số theo PTTT |
| GET | /api/store/analytics/{storeAdminId}/branch-performance | Hiệu suất chi nhánh |
| GET | /api/store/analytics/{storeAdminId}/alerts | Cảnh báo hệ thống |
| GET | /api/store/analytics/{storeAdminId}/payments | Lịch sử thanh toán |
| GET | /api/branch-analytics/today-overview | Tổng quan hôm nay |
| GET | /api/branch-analytics/daily-sales | Doanh số theo ngày |
| GET | /api/branch-analytics/top-products | Sản phẩm bán chạy |
| GET | /api/branch-analytics/top-cashiers | Thu ngân xuất sắc |
| GET | /api/branch-analytics/payment-breakdown | Phân bổ PTTT |
| GET | /api/branch-analytics/category-sales | Doanh số theo danh mục |

*Bảng 4.37 API nhóm Thống kê*

#### O. Nhóm Quản trị hệ thống (AdminDashboardController)

| Phương thức | URL | Mô tả |
|-------------|-----|-------|
| GET | /api/super-admin/dashboard/summary | Tổng quan hệ thống |
| GET | /api/super-admin/dashboard/store-registrations | Thống kê đăng ký |
| GET | /api/super-admin/dashboard/store-status-distribution | Phân bổ trạng thái |
| GET | /api/super-admin/users | Danh sách người dùng |
| GET | /api/super-admin/users/list | Danh sách chi tiết |
| PUT | /api/super-admin/users/{userId} | Cập nhật người dùng |
| GET | /api/super-admin/admin/count | Số lượng admin |
| GET | /api/super-admin/admin/expiring | Subscription sắp hết hạn |

*Bảng 4.38 API nhóm Quản trị hệ thống*


## 4.3 Thiết kế giao diện người dùng

Giao diện hệ thống Zosh POS được xây dựng bằng React.js (Vite), sử dụng ShadCN UI làm thư viện component, Redux Toolkit quản lý state, và hỗ trợ Dark/Light mode. Giao diện được phân chia thành các nhóm màn hình theo vai trò người dùng.

### 4.3.1 Danh sách các nhóm giao diện

| STT | Nhóm giao diện | Vai trò truy cập | Số màn hình | Mô tả |
|-----|---------------|------------------|-------------|-------|
| 1 | Landing Page | Công khai | 1 | Trang giới thiệu hệ thống |
| 2 | Xác thực | Công khai | 3 | Đăng nhập, Đăng ký, Quên mật khẩu |
| 3 | Onboarding | Store Admin | 2 | Thiết lập cửa hàng lần đầu |
| 4 | Store Dashboard | Store Admin | 12 | Bảng điều khiển chủ cửa hàng |
| 5 | POS Cashier | Branch Cashier | 5 | Giao diện bán hàng tại quầy |
| 6 | Branch Manager | Branch Manager | 3 | Quản lý chi nhánh |
| 7 | Super Admin | Admin | 4 | Quản trị toàn hệ thống |

*Bảng 4.39 Danh sách nhóm giao diện*

### 4.3.2 Chi tiết các màn hình chính

#### 4.3.2.1 Nhóm Xác thực

| STT | Tên màn hình | File | Mô tả |
|-----|-------------|------|-------|
| 1 | Đăng nhập | Login.jsx | Form nhập email/password, nút đăng nhập, link đăng ký |
| 2 | Đăng ký | Login.jsx (tab) | Form đăng ký: fullName, email, password, phone, role |
| 3 | Đặt lại mật khẩu | ResetPassword.jsx | Form nhập email → Xác thực OTP → Đổi mật khẩu mới |

*Bảng 4.40 Màn hình nhóm Xác thực*

#### 4.3.2.2 Nhóm Onboarding

| STT | Tên màn hình | File | Mô tả |
|-----|-------------|------|-------|
| 1 | Thông tin chủ cửa hàng | OwnerDetailsForm.jsx | Nhập họ tên, email, SĐT |
| 2 | Thông tin cửa hàng | StoreDetailsForm.jsx | Nhập tên thương hiệu, loại cửa hàng, địa chỉ |

*Bảng 4.41 Màn hình nhóm Onboarding*

#### 4.3.2.3 Nhóm Store Dashboard (Chủ cửa hàng)

| STT | Tên màn hình | File | Mô tả |
|-----|-------------|------|-------|
| 1 | Dashboard | StoreDashboard.jsx | Tổng quan doanh số, biểu đồ, đơn hàng gần đây |
| 2 | Quản lý Chi nhánh | Branches.jsx | Danh sách, thêm/sửa/xóa chi nhánh |
| 3 | Quản lý Sản phẩm | Products.jsx | Danh sách, thêm/sửa/xóa sản phẩm, tìm kiếm |
| 4 | Quản lý Danh mục | Categories.jsx | Danh sách, thêm/sửa/xóa danh mục |
| 5 | Quản lý Nhân viên | StoreEmployees.jsx | Danh sách, thêm/sửa/xóa nhân viên, phân quyền |
| 6 | Thông tin Cửa hàng | Stores.jsx | Xem/sửa thông tin cửa hàng, liên hệ |
| 7 | Báo cáo | Reports.jsx | Báo cáo doanh số, xu hướng, hiệu suất chi nhánh |
| 8 | Doanh số | Sales.jsx | Phân tích doanh số theo ngày/tháng/chi nhánh |
| 9 | Cảnh báo | Alerts.jsx | Tồn kho thấp, nhân viên không hoạt động, hoàn trả đột biến |
| 10 | Cài đặt | Settings.jsx | Cài đặt cửa hàng, bảo mật, thông báo, thanh toán |
| 11 | Nâng cấp gói | Upgrade.jsx | Chọn và thanh toán gói dịch vụ |

*Bảng 4.42 Màn hình nhóm Store Dashboard*

#### 4.3.2.4 Nhóm POS Cashier (Thu ngân)

| STT | Tên màn hình | File | Mô tả |
|-----|-------------|------|-------|
| 1 | Giao diện POS | POSPage.jsx | Bàn phím bán hàng, giỏ hàng, thanh toán nhanh |
| 2 | Quản lý Tồn kho | Inventory.jsx | Xem/cập nhật tồn kho tại chi nhánh |
| 3 | Lịch sử Đơn hàng | OrderHistory.jsx | Xem danh sách đơn đã bán |
| 4 | Hoàn trả | RefundPage.jsx | Tìm đơn hàng, tạo hoàn trả, in phiếu |
| 5 | Ca làm việc | ShiftReportPage.jsx | Bắt đầu/kết thúc ca, xem báo cáo ca |

*Bảng 4.43 Màn hình nhóm POS Cashier*

#### 4.3.2.5 Nhóm Branch Manager (Quản lý chi nhánh)

| STT | Tên màn hình | File | Mô tả |
|-----|-------------|------|-------|
| 1 | Dashboard Chi nhánh | BranchDashboard.jsx | Tổng quan doanh số chi nhánh hôm nay |
| 2 | Quản lý Nhân viên CN | BranchEmployees.jsx | Danh sách nhân viên chi nhánh |
| 3 | Quản lý Tồn kho CN | BranchInventory.jsx | Tồn kho tại chi nhánh |

*Bảng 4.44 Màn hình nhóm Branch Manager*

#### 4.3.2.6 Nhóm Super Admin (Quản trị viên)

| STT | Tên màn hình | File | Mô tả |
|-----|-------------|------|-------|
| 1 | Dashboard Admin | SuperAdminDashboard.jsx | Tổng quan toàn hệ thống: cửa hàng, người dùng, doanh thu |
| 2 | Quản lý Cửa hàng | StoreManagement.jsx | Duyệt/Chặn cửa hàng |
| 3 | Quản lý Gói dịch vụ | PlanManagement.jsx | Thêm/sửa/xóa gói subscription |
| 4 | Quản lý Người dùng | UserManagement.jsx | Danh sách và quản lý tất cả người dùng |

*Bảng 4.45 Màn hình nhóm Super Admin*

### 4.3.3 Sơ đồ điều hướng tổng quát

```
Landing Page → Đăng nhập / Đăng ký
                    │
         ┌──────────┼──────────────┐
         ▼          ▼              ▼
    Store Admin  Branch Cashier  Super Admin
         │          │              │
    Onboarding   POS Page      Dashboard
         │          │              │
    Dashboard    ├─ Tồn kho    ├─ Cửa hàng
    ├─ CN        ├─ Đơn hàng   ├─ Gói DV
    ├─ SP        ├─ Hoàn trả   └─ Users
    ├─ DM        └─ Ca LV
    ├─ NV
    ├─ Báo cáo
    ├─ Cảnh báo
    └─ Cài đặt
```

*Hình 4.2 Sơ đồ điều hướng tổng quát*

## 4.4 Thiết kế bảo mật

### 4.4.1 Xác thực (Authentication)

Hệ thống sử dụng **JWT (JSON Web Token)** để xác thực người dùng:

- **Đăng nhập**: Người dùng gửi email/password → Server xác thực → Trả về JWT token
- **JWT Provider**: Lớp `JwtProvider` sử dụng thuật toán HS256 với secret key để tạo và xác thực token
- **Token Storage**: JWT được lưu tại `localStorage` phía client, gửi kèm trong header `Authorization: Bearer <token>` mỗi request
- **Password Encryption**: Mật khẩu được mã hóa bằng **BCryptPasswordEncoder** trước khi lưu vào database

### 4.4.2 Phân quyền (Authorization)

Hệ thống phân quyền dựa trên vai trò (Role-Based Access Control - RBAC):

| Vai trò | Quyền hạn |
|---------|-----------|
| ROLE_ADMIN | Toàn quyền quản trị hệ thống, duyệt cửa hàng, quản lý gói dịch vụ |
| ROLE_STORE_ADMIN | Quản lý cửa hàng, chi nhánh, sản phẩm, nhân viên, xem báo cáo |
| ROLE_STORE_MANAGER | Quản lý cửa hàng (quyền hạn chế hơn Store Admin) |
| ROLE_BRANCH_MANAGER | Quản lý chi nhánh, xem thống kê chi nhánh |
| ROLE_BRANCH_ADMIN | Quản lý nghiệp vụ chi nhánh |
| ROLE_BRANCH_CASHIER | Bán hàng POS, quản lý ca, hoàn trả |
| ROLE_CUSTOMER | Xem thông tin cá nhân |

*Bảng 4.46 Phân quyền theo vai trò*

### 4.4.3 Bảo mật API

- **CORS Configuration**: Cho phép cross-origin từ frontend domain
- **CSRF Protection**: Tắt CSRF do sử dụng stateless JWT
- **Request Filtering**: `JwtTokenValidator` filter kiểm tra token mỗi request
- **Password Reset**: Token UUID có thời hạn 5 phút, xóa sau khi sử dụng

## 4.5 Thiết kế kiến trúc triển khai

### 4.5.1 Mô hình triển khai

```
┌─────────────────────────────────────────────────────┐
│                    CLIENT TIER                       │
│  ┌───────────────────────────────────────────────┐   │
│  │         React.js (Vite) - SPA                 │   │
│  │  ├── Redux Toolkit (State Management)         │   │
│  │  ├── Axios (HTTP Client)                      │   │
│  │  ├── ShadCN UI (Component Library)            │   │
│  │  └── React Router DOM (Navigation)            │   │
│  └───────────────────────────────────────────────┘   │
│                    Port: 5173                        │
└─────────────────────┬───────────────────────────────┘
                      │ REST API (JSON)
                      │ JWT Authentication
┌─────────────────────▼───────────────────────────────┐
│                   SERVER TIER                        │
│  ┌───────────────────────────────────────────────┐   │
│  │         Spring Boot 3.x - REST API            │   │
│  │  ├── Spring Security + JWT                    │   │
│  │  ├── Spring Data JPA (Repository)             │   │
│  │  ├── Hibernate ORM (Entity Mapping)           │   │
│  │  ├── Lombok (Boilerplate Reduction)           │   │
│  │  └── Maven (Build Tool)                       │   │
│  └───────────────────────────────────────────────┘   │
│                    Port: 8080                        │
└─────────────────────┬───────────────────────────────┘
                      │ JDBC
┌─────────────────────▼───────────────────────────────┐
│                   DATA TIER                          │
│  ┌───────────────────────────────────────────────┐   │
│  │              MySQL 8.x                        │   │
│  │              Database: zosh_pos               │   │
│  │              20 Tables                        │   │
│  └───────────────────────────────────────────────┘   │
│                    Port: 3306                        │
└─────────────────────────────────────────────────────┘
```

*Hình 4.3 Kiến trúc triển khai 3 tầng*

### 4.5.2 Cấu hình hệ thống

| Thành phần | Công nghệ | Phiên bản | Port |
|-----------|-----------|-----------|------|
| Frontend | React.js + Vite | React 18 | 5173 |
| Backend | Spring Boot | 3.x | 8080 |
| Database | MySQL | 8.x | 3306 |
| Java | JDK | 17+ | - |
| Node.js | Node | 18+ | - |
| Build Tool | Maven | 3.x | - |
| Package Manager | npm | 9+ | - |

*Bảng 4.47 Cấu hình hệ thống*

