TRƯỜNG ĐH CÔNG NGHỆ GTVT                    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
  Khoa Công nghệ thông tin                      Độc lập – Tự do – Hạnh phúc
___________________________                    ___________________________


                        ĐỀ CƯƠNG ĐỒ ÁN TỐT NGHIỆP
                     Thời gian từ 09/03/2026… đến 31/05/2026…


Họ và tên sinh viên: ................................................................
Mã sinh viên: ...........................................................................
Lớp: ........................... Điện thoại: ...........................................
Email: ......................................................................................
Giảng viên hướng dẫn: ...........................................................

────────────────────────────────────────────────────────────────────────────────

Nội dung đồ án tốt nghiệp:

Xây dựng hệ thống điểm bán hàng (POS) đa chi nhánh cho chuỗi cửa hàng bán lẻ

Hệ thống được xây dựng nhằm cung cấp một nền tảng quản lý bán hàng tập trung cho
các chuỗi cửa hàng bán lẻ, cho phép chủ cửa hàng dễ dàng quản lý nhiều chi nhánh,
nhân viên và hoạt động kinh doanh thông qua một hệ thống thống nhất.

Hệ thống được phát triển trên nền tảng Spring Boot (backend) và React + Vite
(frontend) với các chức năng chính như sau:
- Quản lý cửa hàng và chi nhánh theo mô hình đa chi nhánh (multi-branch).
- Quản lý sản phẩm, danh mục và tồn kho theo từng chi nhánh.
- Quản lý nhân viên và phân quyền theo vai trò.
- Thực hiện bán hàng tại quầy, tạo đơn hàng và xử lý hoàn trả.
- Quản lý ca làm việc và tổng kết doanh thu cuối ca.
- Thống kê và báo cáo kinh doanh theo thời gian thực.

Bên cạnh đó, hệ thống quản trị cho phép cấp Super Admin phê duyệt cửa hàng mới,
quản lý các gói dịch vụ (subscription) và giám sát toàn bộ hoạt động của hệ thống.

Hệ thống được xây dựng sử dụng các công nghệ như Spring Boot, Spring Security,
Spring Data JPA, MySQL, React, Redux Toolkit, Tailwind CSS và shadcn/ui, áp dụng
mô hình kiến trúc REST API kết hợp SPA (Single Page Application) nhằm đảm bảo
tính mở rộng, bảo mật và dễ bảo trì.

Loại hình: Giải pháp trên nền web

────────────────────────────────────────────────────────────────────────────────

Mục đích nghiên cứu:

- Nghiên cứu tổng quan về hệ thống quản lý bán hàng (POS) và mô hình vận hành
  chuỗi cửa hàng bán lẻ đa chi nhánh.
- Tìm hiểu các công nghệ phát triển ứng dụng web hiện đại như Java Spring Boot,
  React, Vite, Redux Toolkit, MySQL và Tailwind CSS.
- Phân tích và thiết kế hệ thống POS đáp ứng đầy đủ nghiệp vụ của chuỗi cửa hàng
  bán lẻ với nhiều vai trò người dùng khác nhau.
- Xây dựng hệ thống cho phép các cấp quản lý theo dõi, điều phối và kiểm soát
  hoạt động kinh doanh trên toàn chuỗi theo thời gian thực.
- Phát triển giao diện thu ngân cho phép tạo đơn hàng, tính tiền, xử lý hoàn trả
  và quản lý ca làm việc một cách nhanh chóng và chính xác.
- Rèn luyện kỹ năng phân tích hệ thống, thiết kế cơ sở dữ liệu quan hệ và phát
  triển ứng dụng web theo mô hình phân tầng (layered architecture).

────────────────────────────────────────────────────────────────────────────────

Dự kiến kết quả:

- Xây dựng được một hệ thống POS đa chi nhánh hoàn chỉnh phục vụ vận hành chuỗi
  cửa hàng bán lẻ.
- Hệ thống hỗ trợ đầy đủ nghiệp vụ: đăng ký cửa hàng, tạo chi nhánh, thêm sản
  phẩm, phân công nhân viên, bán hàng tại quầy và theo dõi tồn kho.
- Hệ thống quản trị cho phép Super Admin duyệt cửa hàng và quản lý gói dịch vụ.
- Giao diện người dùng thân thiện, trực quan, đáp ứng đúng luồng nghiệp vụ thực tế
  của từng vai trò trong hệ thống.
- Hoàn thành báo cáo đồ án tốt nghiệp đúng yêu cầu và bảo vệ thành công trước
  hội đồng.

────────────────────────────────────────────────────────────────────────────────

Phân quyền và chức năng theo vai trò:

► SUPER ADMIN (Quản trị viên hệ thống):
  o Xem danh sách tất cả cửa hàng trên hệ thống
  o Phê duyệt / chặn cửa hàng đăng ký mới
  o Quản lý gói dịch vụ (Subscription Plans)
    - Thêm / Sửa / Xóa gói dịch vụ
    - Cấu hình giới hạn: số chi nhánh, sản phẩm, nhân viên
  o Theo dõi lịch sử thanh toán gói dịch vụ của các cửa hàng

► STORE ADMIN / STORE MANAGER (Chủ cửa hàng / Quản lý cửa hàng):
  o Quản lý thông tin cửa hàng
    - Cập nhật thông tin, địa chỉ, liên hệ
    - Đăng ký và gia hạn gói dịch vụ
  o Quản lý chi nhánh
    - Thêm / Sửa / Xóa chi nhánh
    - Cấu hình giờ mở – đóng cửa, ngày làm việc
  o Quản lý sản phẩm và danh mục
    - Thêm / Sửa / Xóa danh mục
    - Thêm / Sửa / Xóa sản phẩm
    - Upload ảnh sản phẩm
  o Quản lý nhân viên
    - Thêm nhân viên, phân công chi nhánh
    - Phân quyền vai trò (Branch Manager / Cashier)
  o Báo cáo và thống kê
    - Xem doanh thu toàn chuỗi
    - Báo cáo theo chi nhánh, theo thời gian

► BRANCH MANAGER / BRANCH ADMIN (Quản lý chi nhánh):
  o Quản lý tồn kho chi nhánh
    - Xem danh sách tồn kho sản phẩm
    - Cập nhật số lượng tồn kho
  o Quản lý đơn hàng tại chi nhánh
    - Xem danh sách đơn hàng
    - Xem chi tiết đơn hàng
  o Quản lý nhân viên tại chi nhánh
    - Xem danh sách nhân viên
    - Xem ca làm việc của nhân viên
  o Báo cáo chi nhánh
    - Xem doanh thu chi nhánh theo ngày / tuần / tháng
    - Xem top sản phẩm bán chạy

► BRANCH CASHIER (Thu ngân):
  o Quản lý ca làm việc
    - Bắt đầu ca làm việc
    - Kết thúc ca và xem báo cáo tổng kết ca
  o Thực hiện bán hàng
    - Tìm kiếm và chọn sản phẩm
    - Thêm / cập nhật / xóa sản phẩm trong đơn
    - Xem thông tin tồn kho sản phẩm
  o Quản lý khách hàng
    - Tìm kiếm và liên kết thông tin khách hàng
    - Tạo khách hàng mới
  o Thanh toán
    - Thanh toán tiền mặt (CASH)
    - Thanh toán bằng thẻ (CARD)
    - Thanh toán UPI
  o Hoàn trả đơn hàng (Refund)
    - Tìm kiếm đơn hàng cần hoàn trả
    - Nhập lý do hoàn trả
    - Xác nhận hoàn tiền
  o Tra cứu lịch sử đơn hàng trong ca

────────────────────────────────────────────────────────────────────────────────

Lịch trình thực hiện (Bám sát nội dung công việc):

Tuần 1: Khảo sát và nghiên cứu tổng quan
- Tìm hiểu tổng quan về hệ thống POS và mô hình vận hành chuỗi bán lẻ đa chi nhánh.
- Khảo sát và phân tích yêu cầu của hệ thống đối với các vai trò người dùng.
- Xác định các chức năng chính của hệ thống.

Tuần 2: Nghiên cứu công nghệ và kiến trúc hệ thống
- Nghiên cứu các công nghệ: Spring Boot, Spring Security, JPA/Hibernate, MySQL,
  React, Vite, Redux Toolkit, Tailwind CSS.
- Tìm hiểu mô hình REST API, kiến trúc phân tầng và xác thực JWT.

Tuần 3: Phân tích yêu cầu hệ thống
- Phân tích nghiệp vụ và chức năng của hệ thống theo từng vai trò.
- Xây dựng Use Case Diagram mô tả các chức năng của từng loại người dùng.

Tuần 4: Thiết kế mô hình hệ thống
- Xây dựng Sequence Diagram cho các luồng chức năng chính: đăng nhập, tạo đơn
  hàng, bắt đầu/kết thúc ca, hoàn trả đơn hàng.
- Xây dựng Activity Diagram mô tả luồng hoạt động nghiệp vụ của hệ thống.

Tuần 5: Thiết kế cơ sở dữ liệu
- Thiết kế cơ sở dữ liệu cho hệ thống POS đa chi nhánh.
- Xây dựng sơ đồ ERD và các bảng dữ liệu chính: users, stores, branches, products,
  inventories, orders, order_items, shift_report, refund, subscriptions...

Tuần 6: Khởi tạo và cấu hình hệ thống
- Cài đặt môi trường phát triển (Java 17, Node.js, MySQL).
- Khởi tạo project Spring Boot (backend) và React + Vite (frontend).
- Cấu hình Spring Security, JWT, CORS và kết nối database.

Tuần 7: Xây dựng hệ thống xác thực và phân quyền
- Xây dựng chức năng đăng ký, đăng nhập và xác thực bằng JWT.
- Triển khai phân quyền RBAC theo 7 vai trò trong hệ thống.
- Xây dựng chức năng quên mật khẩu và reset mật khẩu qua email.

Tuần 8: Phát triển phân hệ Super Admin và Store Admin
- Xây dựng chức năng phê duyệt / chặn cửa hàng (Super Admin).
- Xây dựng chức năng quản lý gói dịch vụ (Subscription Plans).
- Xây dựng chức năng quản lý cửa hàng, chi nhánh, danh mục và sản phẩm.

Tuần 9: Phát triển phân hệ quản lý nhân viên và tồn kho
- Xây dựng chức năng quản lý nhân viên, phân công chi nhánh và phân quyền vai trò.
- Xây dựng chức năng quản lý tồn kho: xem và cập nhật số lượng theo chi nhánh.

Tuần 10: Phát triển phân hệ thu ngân (Cashier)
- Xây dựng giao diện bán hàng tại quầy: tìm kiếm sản phẩm, thêm vào đơn, tính tiền.
- Xây dựng chức năng quản lý ca làm việc: bắt đầu ca, kết thúc ca, tổng kết ca.
- Xây dựng chức năng xử lý hoàn trả đơn hàng.

Tuần 11: Xây dựng chức năng báo cáo và thống kê
- Xây dựng dashboard thống kê doanh thu cho Store Admin và Branch Manager.
- Xây dựng báo cáo tổng kết ca: doanh thu, số đơn, top sản phẩm bán chạy.
- Tích hợp biểu đồ trực quan bằng thư viện Recharts.

Tuần 12: Kiểm thử, hoàn thiện và chuẩn bị báo cáo
- Kiểm thử và đánh giá các chức năng của hệ thống.
- Hoàn thiện hệ thống và sửa các lỗi phát sinh.
- Hoàn thiện báo cáo đồ án tốt nghiệp và chuẩn bị nội dung bảo vệ.

────────────────────────────────────────────────────────────────────────────────

Kết cấu của ĐATN:

LỜI CAM ĐOAN
MỤC LỤC
DANH MỤC HÌNH VẼ
DANH MỤC BẢNG BIỂU
BẢNG KÝ HIỆU VIẾT TẮT
LỜI MỞ ĐẦU

CHƯƠNG 1. TỔNG QUAN
  1.1 Lý do chọn đề tài
  1.2 Mục tiêu của đề tài
  1.3 Giới hạn và phạm vi đề tài
  1.4 Kết quả dự kiến đặt được

CHƯƠNG 2. CƠ SỞ LÝ THUYẾT
  2.1 Kiến trúc ứng dụng web hiện đại
      2.1.1 Mô hình Client – Server
      2.1.2 Kiến trúc REST API
      2.1.3 Mô hình MVC (Model – View – Controller)
  2.2 Công nghệ Backend
      2.2.1 Java và Spring Boot
      2.2.2 Spring Security và JWT
      2.2.3 Spring Data JPA và Hibernate
  2.3 Cơ sở dữ liệu MySQL
  2.4 Công nghệ Frontend
      2.4.1 React và Vite
      2.4.2 Redux Toolkit
      2.4.3 Tailwind CSS và shadcn/ui
      2.4.4 Recharts
  2.5 Các dịch vụ tích hợp bên ngoài
      2.5.1 Cloudinary — Lưu trữ ảnh
      2.5.2 Razorpay / Stripe — Thanh toán trực tuyến
      2.5.3 Gmail SMTP — Gửi email
  2.6 Công cụ phát triển và triển khai
      2.6.1 Git và GitHub
      2.6.2 Docker
      2.6.3 Postman

CHƯƠNG 3. PHÂN TÍCH HỆ THỐNG
  3.1 Khảo sát hệ thống
      3.1.1 Tổng quan về hệ thống
      3.1.2 Cách thức khảo sát
      3.1.3 Đánh giá hiện trạng
      3.1.4 Dự kiến các chức năng của hệ thống
  3.2 Phân tích hệ thống
      3.2.1 Xác định các tác nhân Actor và chức năng (Usecase)
      3.2.2 Biểu đồ UseCase tổng quát
      3.2.3 Biểu đồ UseCase chi tiết
      3.2.4 Biểu đồ lớp
      3.2.5 Biểu đồ hoạt động
      3.2.6 Biểu đồ tuần tự

CHƯƠNG 4. THIẾT KẾ HỆ THỐNG
  4.1 Thiết kế, xây dựng cơ sở dữ liệu
      4.1.1 Danh sách các bảng dữ liệu
      4.1.2 Chi tiết các bảng dữ liệu
  4.2 Thiết kế giao diện website

KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

TÀI LIỆU THAM KHẢO

────────────────────────────────────────────────────────────────────────────────

Ngày bảo vệ kết quả: .............................................................................................

Ý kiến phê duyệt của người hướng dẫn về nội dung đề cương:
..................................................................................................................................
..................................................................................................................................



        Ngày ...... tháng ...... năm 2026          Ngày ...... tháng ...... năm 2026

         Xác nhận của                                  Sinh viên thực hiện
         giảng viên hướng dẫn


    ....................................           ....................................
