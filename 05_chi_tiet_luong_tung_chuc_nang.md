# 📖 ĐẶC TẢ CHI TIẾT TỪNG CHỨC NĂNG HỆ THỐNG ZOSH POS
*(Từ Giao diện Frontend đến Logic Backend & Database)*

Tài liệu này phân rã toàn bộ hệ thống thành từng **Chức năng cụ thể**. Đối với mỗi chức năng, bạn sẽ thấy rõ luồng đi của dữ liệu từ khi click chuột trên giao diện cho đến khi lưu vào cơ sở dữ liệu.

---

## 1. NHÓM CHỨC NĂNG XÁC THỰC (AUTHENTICATION)

### 1.1 Đăng ký tài khoản (Sign Up)
- **Vai trò:** Người dùng chưa có tài khoản (sẽ trở thành Store Admin).
- **Frontend (React):** 
  - Giao diện: Component `Register.jsx`.
  - Redux: Dispatch action `signup(userData)` trong `authThunks.js`.
- **API Gọi:** `POST /auth/signup`
- **Backend (Spring Boot):**
  - **AuthServiceImpl.java:** 
    - Kiểm tra email đã tồn tại trong bảng `users` chưa.
    - Chặn không cho tự ý đăng ký role `ROLE_ADMIN`.
    - Mã hóa mật khẩu bằng `BCryptPasswordEncoder`.
    - Tạo đối tượng `User` và lưu vào Database.
    - Gọi `JwtProvider` tạo mã JWT token.
- **Kết quả:** Trả về `{ jwt, user }`. Frontend lưu `jwt` vào `localStorage` và điều hướng vào hệ thống.

### 1.2 Đăng nhập (Login)
- **Vai trò:** Mọi user.
- **Frontend:** `Login.jsx` -> dispatch `login(credentials)`.
- **API Gọi:** `POST /auth/login`
- **Backend:**
  - `AuthServiceImpl.java`: Tìm user bằng email (`loadUserByUsername`).
  - Dùng `passwordEncoder.matches()` để so sánh mật khẩu nhập vào và mật khẩu băm trong DB.
  - Sinh JWT Token mới, cập nhật `last_login` vào bảng `users`.
- **Kết quả:** FE nhận token, decode token để biết Role, điều hướng sang đúng Dashboard (Store Admin, Cashier,...).

---

## 2. NHÓM CHỨC NĂNG QUẢN LÝ CỬA HÀNG (STORE MANAGEMENT)

### 2.1 Tạo Cửa Hàng (Onboarding)
- **Vai trò:** Store Admin (mới đăng ký).
- **Frontend:** `CreateStoreForm.jsx` -> dispatch `createStore(storeData)`.
- **API:** `POST /api/stores`
- **Backend:**
  - `JwtValidator` lấy `currentUser` từ token.
  - `StoreServiceImpl`: Tạo thực thể `Store`, gán `storeAdmin = currentUser`.
  - Mặc định set `status = PENDING`.
- **Database:** Insert vào bảng `stores`.

### 2.2 Duyệt Cửa Hàng (Approve Store)
- **Vai trò:** Super Admin.
- **Frontend:** `StoreTable.jsx` -> Nút Approve -> dispatch `moderateStore({id, action})`.
- **API:** `PUT /api/stores/{storeId}/moderate`
- **Backend:** 
  - Kiểm tra quyền (`hasRole('ADMIN')`).
  - Đổi `status` của cửa hàng từ `PENDING` sang `ACTIVE`.

---

## 3. NHÓM CHỨC NĂNG QUẢN LÝ CHI NHÁNH (BRANCH)

### 3.1 Tạo Chi nhánh mới
- **Vai trò:** Store Admin / Store Manager.
- **Frontend:** `BranchForm.jsx` -> dispatch `createBranch(branchDto)`.
- **API:** `POST /api/branches`
- **Backend:**
  - `BranchServiceImpl`: Lấy thông tin Cửa hàng (`store`) mà người dùng hiện tại đang quản lý.
  - Khởi tạo `Branch`, gắn `store_id`, lưu địa chỉ, giờ mở/đóng cửa.
- **Database:** Insert vào bảng `branches`.

---

## 4. NHÓM CHỨC NĂNG QUẢN LÝ SẢN PHẨM & TỒN KHO

### 4.1 Thêm Danh Mục (Category)
- **Vai trò:** Store Admin / Manager.
- **Frontend:** dispatch `createCategory({name})`.
- **API:** `POST /api/categories`
- **Backend:** Tạo record trong bảng `categories`, liên kết với `store_id`.

### 4.2 Thêm Sản Phẩm (Product)
- **Vai trò:** Store Admin / Manager.
- **Frontend:** 
  - Nhập thông tin: Tên, Mã SKU, Giá gốc (MRP), Giá bán (Selling Price), Hình ảnh.
  - Ảnh được upload trực tiếp lên Cloudinary từ JS (`uploadToCloudinary.js`), nhận về URL ảnh.
  - dispatch `createProduct(productDto)`.
- **API:** `POST /api/products`
- **Backend:**
  - `ProductServiceImpl`: Kiểm tra user có quyền quản lý Store này không.
  - Tìm Category tương ứng.
  - Lưu thực thể `Product` vào DB kèm URL ảnh.
- **Database:** Bảng `products`.

### 4.3 Đồng bộ Tồn Kho (Inventory)
- *Lưu ý: Hệ thống này tồn kho được gắn với từng Chi nhánh (Branch).*
- **Backend Logic:** Khi tạo sản phẩm hoặc nhập hàng, bảng `inventories` sẽ tạo một record chứa `branch_id`, `product_id` và `quantity`.

---

## 5. NHÓM CHỨC NĂNG QUẢN LÝ NHÂN SỰ (EMPLOYEE)

### 5.1 Thêm Nhân viên
- **Vai trò:** Store Admin / Manager.
- **Frontend:** Chọn Role (Thu ngân, Quản lý chi nhánh) -> Cấp vào Chi nhánh nào -> Nhập email/tên.
  - dispatch `addEmployee(userDto)`.
- **API:** `POST /api/stores/add/employee`
- **Backend:**
  - `EmployeeServiceImpl`: Tạo tài khoản `User` mới.
  - Set `store_id` (Cửa hàng hiện tại) và `branch_id` (Chi nhánh được chỉ định).
  - Encode mật khẩu tự động (VD: pass mặc định 123456).
  - Nếu role là `BRANCH_MANAGER`, cập nhật bảng `branches`, set `manager_id` = user mới.

---

## 6. 🔥 CHỨC NĂNG CỐT LÕI: POS (BÁN HÀNG TẠI QUẦY)

*Đây là luồng quan trọng và phức tạp nhất, kết hợp mạnh mẽ giữa Redux (Frontend) và API (Backend).*

### 6.1 Bắt Đầu Ca (Start Shift)
- **Vai trò:** Thu ngân (Cashier).
- **Frontend:** Nút "Start Shift" -> dispatch `startShift()`.
- **API:** `POST /api/shift-reports/start?branchId=...`
- **Backend (`ShiftReportServiceImpl`):**
  - Kiểm tra hôm nay Cashier này đã có ca làm việc chưa. Nếu có (chưa kết thúc) -> ném lỗi `Shift already started today`.
  - Nếu chưa, tạo bản ghi `ShiftReport` với `shiftStart = now()`, `cashier_id`, `branch_id`.

### 6.2 Thao tác Giỏ hàng (Cart) - Hoàn Toàn Tại Frontend
- Trải nghiệm POS yêu cầu không có độ trễ.
- **Frontend (`cartSlice.js`):**
  - Click món ăn -> Action `addItem`: Tăng `quantity` trong mảng `items`.
  - Nhập giảm giá, thuế -> Action `setDiscount`, `setTaxRate`.
  - **Tính tiền Realtime (Local State):** Reducer tự động tính:
    - `subtotal = sum(sellingPrice * qty)`
    - `discountAmount = subtotal * %`
    - `total = subtotal - discountAmount + tax`
  - *Lưu ý: Chưa hề có API nào gọi về backend ở bước này.*

### 6.3 Tạm giữ đơn (Hold Order)
- Khách chưa trả tiền ngay -> Nhấn "Hold".
- **Frontend (`cartSlice.js`):** Action `holdOrder` bốc toàn bộ `items` hiện tại nhét vào mảng `holdOrders`, sau đó làm trống giỏ hàng hiện tại.

### 6.4 Thanh Toán (Checkout & Tạo Đơn)
- **Frontend:** Nhấn "Thanh toán", chọn tiền mặt/thẻ -> dispatch `createOrder(cartData)`.
- **API:** `POST /api/orders` (Gửi payload gồm `paymentType`, mảng `items` gồm `productId` & `quantity`).
- **Backend (`OrderServiceImpl`):**
  - `cashier = getCurrentUser()`, `branch = cashier.getBranch()`.
  - Tạo thực thể `Order` (status = `COMPLETED`).
  - Vòng lặp duyệt mảng items: Lấy giá sản phẩm thực tế từ DB (`sellingPrice`) nhân với `quantity` để ra thành tiền (tránh Frontend bị hack sửa giá).
  - Lưu chi tiết vào bảng `order_items`.
  - *Lưu ý: Khi hoàn tất, Backend phản hồi OK. Frontend dispatch `clearCart()` để dọn giỏ hàng, sẵn sàng đón khách tiếp theo.*

---

## 7. NHÓM CHỨC NĂNG HOÀN TRẢ (REFUND)

### 7.1 Tạo Hoàn Trả
- **Vai trò:** Cashier / Branch Manager.
- **Frontend:** Vào lịch sử đơn hàng -> Chọn "Refund" -> Nhập lý do.
- **API:** `POST /api/refunds`
- **Backend (`RefundServiceImpl`):**
  - Tìm `Order` theo ID.
  - Tạo bản ghi `Refund` gồm `reason`, `amount` (bằng tổng tiền đơn), `cashier_id`.
  - Quan trọng: Cập nhật `status` của Order thành `REFUNDED`.

---

## 8. 🔥 CHỨC NĂNG ĐÓNG CA (END SHIFT & CHỐT SỔ)

### 8.1 Kết Thúc Ca
- **Vai trò:** Cashier.
- **Frontend:** Nhấn "End Shift" -> dispatch `endShift()`.
- **API:** `PATCH /api/shift-reports/end`
- **Backend (`ShiftReportServiceImpl`):** *Logic tính toán hạng nặng*
  1. Tìm ca đang mở của Cashier. Cập nhật `shiftEnd = now()`.
  2. Query DB: Lấy TẤT CẢ `Order` của cashier này trong chi nhánh này tạo từ `shiftStart` đến `shiftEnd`.
  3. Query DB: Lấy TẤT CẢ `Refund` tương tự.
  4. Tính toán: 
     - `totalSales` = Tổng tiền orders.
     - `totalRefunds` = Tổng tiền hoàn.
     - `netSales` = `totalSales - totalRefunds`.
  5. Trích xuất: Tìm 5 sản phẩm bán chạy nhất trong ca. Phân loại doanh thu theo Cash/Card.
  6. Lưu vào DB bảng `shift_report`. Trả về báo cáo tổng kết in ra giấy cho thu ngân.

---

## 9. NHÓM CHỨC NĂNG SUBSCRIPTION & THANH TOÁN (SAAS)

### 9.1 Đăng ký Gói Dịch vụ (Subscribe)
- **Vai trò:** Store Admin.
- **API:** `POST /api/subscriptions/subscribe`
- **Backend:** 
  - `SubscriptionServiceImpl`: Gắn `plan_id` vào `store_id`. Trạng thái `PENDING`.
  - Gọi `PaymentServiceImpl.initiatePayment()`.
  - Tạo link thanh toán thông qua cổng **Razorpay / Stripe**.
  - Trả về `checkoutUrl` cho Frontend mở tab thanh toán.

### 9.2 Xác minh Thanh toán
- **API:** `POST /api/payments/verify`
- **Backend:** Dùng `payment_id` gọi lại API của Razorpay để kiểm tra trạng thái thực tế. Nếu `captured` -> Đổi `Payment` status sang `SUCCESS`, đổi `Subscription` sang `ACTIVE`.

---

## 10. NHÓM CHỨC NĂNG BÁO CÁO (ANALYTICS)

*Sử dụng các Native Queries phức tạp trong Database.*

### 10.1 Báo cáo theo Chi nhánh (Branch Manager)
- **API:** `/api/branch-analytics/daily-sales`
- **Logic Backend:** Dùng vòng lặp `for`, tính tổng `totalAmount` trong bảng `orders` của `branch_id` tương ứng cho từng ngày trong khoảng thời gian được chọn.
- **Frontend:** Dùng thư viện `Recharts` để vẽ biểu đồ đường (Line Chart).

### 10.2 Báo cáo Tổng thể (Store Admin)
- **API:** `/api/store/analytics/...`
- **Logic Backend:** Query tất cả `branch_id` thuộc `store_admin_id`. Group data theo Category (Danh mục), theo Payment Method (Phương thức thanh toán) để trả về mảng dữ liệu.
- **Frontend:** Vẽ biểu đồ tròn (Pie Chart) và biểu đồ cột (Bar Chart). Lấy danh sách nhân viên Inactive (Không login > 7 ngày) hiển thị cảnh báo.

---
**Tổng kết:** Toàn bộ hệ thống Zosh POS là sự kết hợp hoàn hảo giữa **Redux Local State** (giúp giao diện cực nhanh, không lag) và **Spring Boot Backend Security** (giúp xác thực dữ liệu chặt chẽ, truy vấn chốt ca chính xác, an toàn bảo mật nhiều khách thuê Multi-tenant).
