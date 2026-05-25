# 🎤 KỊCH BẢN THUYẾT TRÌNH & DEMO ĐỒ ÁN: ZOSH POS

> **Mục tiêu:** Tài liệu này được thiết kế như một kịch bản "cầm tay chỉ việc" giúp bạn tự tin thuyết trình và demo hệ thống trước hội đồng. Tập trung vào "Business Flow" (Luồng nghiệp vụ) thay vì chỉ nói về code.

---

## 🌟 PHẦN 1: GIỚI THIỆU TỔNG QUAN (Nói trong 2-3 phút)

**Slide/Lời nói:**
> "Kính thưa hội đồng, đề án của em là **Hệ thống Quản lý Điểm bán hàng (POS) Đa chi nhánh - Zosh POS**. Khác với các hệ thống POS đơn lẻ, đây là mô hình **SaaS (Software as a Service)**, cho phép nhiều doanh nghiệp/cửa hàng cùng đăng ký sử dụng trên một nền tảng. Mỗi doanh nghiệp lại có thể quản lý nhiều chi nhánh, nhiều nhân viên với hệ thống phân quyền chặt chẽ từ Super Admin đến Thu ngân (Cashier)."

**Nhấn mạnh 3 điểm nổi bật:**
1. **Kiến trúc Multi-tenant:** Dữ liệu của các cửa hàng được phân tách logic rõ ràng (qua `store_id`, `branch_id`), đảm bảo bảo mật.
2. **Luồng bán hàng chuyên nghiệp:** Tích hợp quản lý ca làm việc (Shift), gộp đơn, tính thuế, giảm giá realtime và xử lý hoàn trả.
3. **Dashboard Realtime:** Thống kê doanh thu, sản phẩm bán chạy, hiệu suất thu ngân chi tiết theo từng chi nhánh và toàn hệ thống.

---

## 💻 PHẦN 2: KỊCH BẢN DEMO THỰC TẾ TRÊN MÀN HÌNH

Dưới đây là **6 luồng chính** bạn nên lần lượt thực hiện khi Demo.

### 🌊 LUỒNG 1: ONBOARDING - TẠO CỬA HÀNG MỚI (Super Admin & Store Admin)
*Mục đích: Chứng minh khả năng quản lý mô hình SaaS.*

1. **Đăng nhập Super Admin** (email: `codewithzosh@gmail.com`).
   - Mở màn hình Dashboard Super Admin: Chỉ ra số lượng cửa hàng PENDING/ACTIVE.
2. **Đăng ký Store Admin mới** (Mở tab ẩn danh).
   - Sign up một tài khoản mới (VD: `ceo@thecoffeehouse.com`).
   - Lúc này, hệ thống sẽ tự động tạo một thực thể `Store` với trạng thái là `PENDING`.
3. **Duyệt cửa hàng (Approve)**
   - Quay lại màn hình Super Admin, vào mục "Stores".
   - Bấm duyệt cửa hàng vừa tạo sang `ACTIVE`.
4. **Đăng ký gói dịch vụ (Subscription)**
   - Sang màn hình Store Admin, báo hệ thống yêu cầu đăng ký gói.
   - Demo việc chọn gói (VD: "Pro Plan") và hiển thị link thanh toán (Stripe/Razorpay flow).

---

### 🌊 LUỒNG 2: SETUP CỬA HÀNG (Store Admin)
*Mục đích: Chứng minh khả năng thiết lập dữ liệu nền tảng.*

1. **Đăng nhập bằng tài khoản Store Admin** (đã duyệt).
2. **Tạo Chi nhánh (Branch)**
   - Vào mục Branches -> Tạo chi nhánh "Chi nhánh Quận 1" (Nhập thông tin địa chỉ, giờ mở/đóng cửa).
3. **Tạo Danh mục & Sản phẩm (Catalog)**
   - Tạo danh mục: "Cà phê", "Trà".
   - Tạo sản phẩm: "Cà phê sữa đá" (SKU: `CFS01`, Giá: `35000`), upload ảnh. Nhấn mạnh việc lưu ảnh qua Cloudinary.
4. **Tạo Nhân viên (Employee)**
   - Vào mục Employees -> Thêm nhân viên mới.
   - Tạo 1 người là `Branch Manager` (gán vào Chi nhánh Q1).
   - Tạo 1 người là `Cashier` (gán vào Chi nhánh Q1).

---

### 🌊 LUỒNG 3: VẬN HÀNH BÁN HÀNG TẠI QUẦY (Cashier) - LUỒNG QUAN TRỌNG NHẤT
*Mục đích: Demo core business của dự án (POS).*

1. **Đăng nhập bằng tài khoản Cashier**.
2. **Bắt đầu ca làm việc (Start Shift)**
   - Hệ thống sẽ chặn không cho bán hàng nếu chưa mở ca.
   - Nhấn "Start Shift". Giải thích: "Hệ thống ghi nhận thời gian bắt đầu ca để chốt doanh thu cuối ngày. Mỗi thu ngân chỉ được mở 1 ca/ngày để tránh gian lận".
3. **Thực hiện bán hàng (POS Interface)**
   - Vào màn hình POS.
   - Click chọn các sản phẩm (VD: 2 Cà phê sữa, 1 Trà đào).
   - *Demo tính năng Giỏ hàng (Cart):*
     - Tăng/giảm số lượng.
     - Add tax (10% VAT).
     - Add discount (Giảm 10%).
     - Dừng lại 5 giây để hội đồng xem con số `Total` tự động nhảy. (Giải thích: "Toàn bộ logic này được tính toán realtime bằng Redux Store ở frontend để đảm bảo tốc độ tối đa cho thu ngân").
4. **Thanh toán (Checkout)**
   - Bấm thanh toán, chọn hình thức "CASH" (Tiền mặt).
   - Hệ thống báo thành công -> In ra màn hình hóa đơn (hoặc chuyển sang màn hình Order Success).
   - *Backend logic (bạn có thể nói thêm):* "Lúc này Backend sẽ lưu Order với status `COMPLETED`, lưu chi tiết từng OrderItem và trừ số lượng Inventory".

---

### 🌊 LUỒNG 4: TẠM GIỮ ĐƠN & HOÀN TRẢ (Tính năng nâng cao)
*Mục đích: Lấy điểm cộng bằng các tính năng sát thực tế.*

1. **Tạm giữ đơn (Hold Order)**
   - Tại màn hình POS, chọn vài món.
   - Nhấn "Hold Order". Giải thích: "Tính năng này giải quyết bài toán khách đang gọi món nhưng quên ví, thu ngân có thể tạm lưu đơn để tính tiền cho khách tiếp theo, không làm tắc nghẽn hàng đợi".
   - Chọn khách khác, thanh toán xong. Mở lại "Hold Orders" và khôi phục đơn cũ.
2. **Hoàn trả (Refund)**
   - Vào lịch sử đơn hàng (Orders).
   - Chọn đơn vừa bán, nhấn "Refund".
   - Nhập lý do: "Khách đổi ý".
   - Giải thích: "Hệ thống sẽ chuyển trạng thái đơn hàng sang `REFUNDED` và ghi nhận một record vào bảng `Refund`. Số tiền này sẽ được trừ vào tổng doanh thu ca của thu ngân".

---

### 🌊 LUỒNG 5: KẾT CA & BÁO CÁO (End Shift & Analytics)
*Mục đích: Cho thấy hệ thống xử lý số liệu chính xác.*

1. **Đóng ca (End Shift) - Giao diện Cashier**
   - Bấm "End Shift".
   - *Giải thích luồng Backend cực hay:* "Khi kết ca, Backend sẽ query toàn bộ đơn hàng và hoàn trả của thu ngân đó trong khoảng thời gian từ lúc Start Shift đến hiện tại. Nó tự động tính: `Tổng Thu`, `Tổng Hoàn Trả`, `Doanh Thu Thuần` và thống kê luôn các mặt hàng bán chạy nhất trong ca. Thu ngân in phiếu này để bàn giao tiền mặt".
2. **Xem báo cáo - Giao diện Branch Manager / Store Admin**
   - Đăng nhập bằng `Branch Manager` hoặc `Store Admin`.
   - Vào tab **Analytics / Dashboard**.
   - Show các biểu đồ:
     - Biểu đồ doanh thu 7 ngày (Daily Sales).
     - Top Cashiers (Ai bán được nhiều nhất).
     - Payment Breakdown (% thanh toán Tiền mặt vs Chuyển khoản).
   - *Nói thêm:* "Các biểu đồ này được lấy từ các API riêng biệt trên Backend (`BranchAnalyticsService`), dữ liệu được group theo thời gian và danh mục bằng SQL queries phức tạp".

---

## 🗣️ PHẦN 3: CÁCH TRẢ LỜI CÂU HỎI PHẢN BIỆN (Q&A)

Hội đồng thường sẽ hỏi để kiểm tra xem bạn có thực sự hiểu hệ thống hay không. Dưới đây là cách đối phó:

**Câu hỏi 1: Hệ thống của em phân quyền như thế nào? Làm sao đảm bảo Chi nhánh A không xem được dữ liệu Chi nhánh B?**
> **Trả lời:** "Hệ thống dùng mô hình RBAC (Role-Based Access Control) kết hợp Data Filtering.
> - Về Role: Em dùng `@PreAuthorize` của Spring Security để chặn API (VD: Thu ngân không được gọi API tạo sản phẩm).
> - Về Data: Khi lấy danh sách Order, em không lấy tất cả. Service sẽ đọc `jwt_token`, lấy ra `currentUser`, từ đó lấy được `branch_id` của user đó. SQL query sẽ có thêm điều kiện `WHERE branch_id = ?`. Do đó, Chi nhánh A không thể thấy dữ liệu của Chi nhánh B dù có cố tình gọi API."

**Câu hỏi 2: Tại sao phần tính tiền Giỏ hàng (Cart) lại để ở Frontend mà không để Backend tính?**
> **Trả lời:** "Trong nghiệp vụ POS, thu ngân cần thao tác cực kỳ nhanh (thêm/bớt món, thêm mã giảm giá liên tục). Nếu mỗi thao tác đều gọi API về Backend tính toán sẽ sinh ra độ trễ (latency), trải nghiệm người dùng sẽ rất tệ. Do đó, em sử dụng Redux Toolkit lưu Local State để tính toán realtime (Subtotal, Tax, Discount). Khi thu ngân bấm Thanh toán, gói JSON cuối cùng mới được đẩy xuống Backend. Backend vẫn sẽ có bước validate lại giá sản phẩm (`sellingPrice` x `quantity`) trước khi lưu vào Database để chống gian lận."

**Câu hỏi 3: Tính năng mở ca/đóng ca (Shift) hoạt động thế nào? Tránh trùng ca ra sao?**
> **Trả lời:** "Bảng `shift_report` có các cột `shift_start` và `shift_end`. Khi bắt đầu ca, em tạo record mới với `shift_end = null`. Nếu thu ngân bấm Start Shift lần nữa, backend sẽ check xem có ca nào đang `shift_end = null` không, nếu có sẽ ném lỗi. Khi đóng ca, Backend sẽ update `shift_end = now()` và query toàn bộ bảng `orders` của thu ngân đó với điều kiện `created_at BETWEEN shift_start AND shift_end` để chốt sổ."

**Câu hỏi 4: JWT token hết hạn thì sao? Em quản lý đăng nhập thế nào?**
> **Trả lời:** "Server tạo JWT mã hóa chứa `email` và `role`, hết hạn sau 24h. Frontend lưu vào `localStorage`. Filter `JwtValidator` của Spring Security sẽ hứng mọi request để kiểm tra. Nếu token hết hạn, backend trả về 401, frontend sẽ tự động catch lỗi và đá user về trang Login."

---

## 🎯 TIPS THUYẾT TRÌNH (Cho người không tự tin)

1. **Chuẩn bị sẵn dữ liệu (Seeding):** Đừng lên demo mới ngồi tạo từ đầu (rất mất thời gian). Hãy tạo sẵn 1 Store, vài Branch, vài chục món ăn, và bắn sẵn vài đơn hàng ngày hôm qua để biểu đồ Analytics có dữ liệu hiển thị. Khi demo chỉ cần tạo 1 đơn hàng mới.
2. **Chia hai màn hình (nếu có thể):** Mở 2 trình duyệt ẩn danh. Trình duyệt 1 đăng nhập Store Admin. Trình duyệt 2 đăng nhập Cashier. Để thấy tính thời gian thực.
3. **Mở DevTools (F12) tab Network:** Khi bấm thanh toán, mở sẵn tab Network để cho hội đồng thấy bạn gọi API thật (`POST /api/orders`) và response trả về JSON đàng hoàng, chứng minh đây không phải giao diện tĩnh.
4. **Hiểu rõ Code:** Nếu hội đồng bắt mở code.
   - Code FE: Mở file `App.jsx` để chỉ Routing, mở `orderThunks.js` để chỉ chỗ gọi API, mở `cartSlice.js` để chỉ chỗ tính tiền.
   - Code BE: Mở `OrderServiceImpl.java` (hàm `createOrder`), mở `ShiftReportServiceImpl.java` (hàm `closeShift`), và `JwtValidator.java` (chỗ kiểm tra Token).
