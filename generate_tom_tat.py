#!/usr/bin/env python3
"""Generate graduation thesis summary (Tóm tắt đồ án tốt nghiệp) as DOCX."""

from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn


def set_run_font(run, name="Times New Roman", size=13, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = p.add_run(text)
    if level == 1:
        set_run_font(run, size=14, bold=True)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        set_run_font(run, size=13, bold=True)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p


def add_body(doc, text, indent=False, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(0)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        p.paragraph_format.first_line_indent = Cm(1.27)
    run = p.add_run(text)
    set_run_font(run, bold=bold)
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.left_indent = Cm(1.27)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    set_run_font(run)
    return p


def setup_document():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
    return doc


def build_document():
    doc = setup_document()

    # ===== TRANG BÌA / TIÊU ĐỀ =====
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ GTVT\n")
    set_run_font(r, size=13, bold=True)
    r = title.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n\n")
    set_run_font(r, size=13, bold=True)

    r = title.add_run("TÓM TẮT ĐỒ ÁN TỐT NGHIỆP\n\n")
    set_run_font(r, size=16, bold=True)

    r = title.add_run(
        "XÂY DỰNG HỆ THỐNG ĐIỂM BÁN HÀNG (POS)\n"
        "ĐA CHI NHÁNH CHO CHUỖI CỬA HÀNG BÁN LẺ\n"
        "(ZOSH POS)\n"
    )
    set_run_font(r, size=14, bold=True)

    doc.add_paragraph()

    info_lines = [
        ("Họ và tên sinh viên:", "..............................................................."),
        ("Mã sinh viên:", ".........................................................................."),
        ("Lớp:", "..........................."),
        ("Ngành đào tạo:", "Công nghệ thông tin"),
        ("Khoa:", "Công nghệ thông tin"),
        ("Giảng viên hướng dẫn:", "ThS. Phạm Văn A"),
    ]
    for label, value in info_lines:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        r1 = p.add_run(f"{label} ")
        set_run_font(r1, bold=True)
        r2 = p.add_run(value)
        set_run_font(r2)

    doc.add_page_break()

    # ===== 1. THÔNG TIN SINH VIÊN =====
    add_heading(doc, "1. THÔNG TIN SINH VIÊN")
    add_body(doc, "Họ và tên: ...............................................................", indent=True)
    add_body(doc, "Mã sinh viên: ..........................................................................", indent=True)
    add_body(doc, "Lớp: ...........................", indent=True)
    add_body(doc, "Ngành đào tạo: Công nghệ thông tin", indent=True)
    add_body(doc, "Khoa: Công nghệ thông tin", indent=True)
    add_body(doc, "Giảng viên hướng dẫn: ThS. Phạm Văn A", indent=True)

    # ===== 2. TÊN ĐỀ TÀI =====
    add_heading(doc, "2. TÊN ĐỀ TÀI", level=2)
    add_body(
        doc,
        "Xây dựng hệ thống điểm bán hàng (POS) đa chi nhánh cho chuỗi cửa hàng bán lẻ — Zosh POS.",
        indent=True,
    )

    # ===== 3. MỤC TIÊU =====
    add_heading(doc, "3. MỤC TIÊU CỦA ĐỀ TÀI", level=2)
    add_body(
        doc,
        "Đề tài hướng tới xây dựng một nền tảng quản lý bán hàng tập trung trên web, phục vụ mô hình "
        "chuỗi cửa hàng bán lẻ đa chi nhánh theo hướng SaaS (Software as a Service). Hệ thống giải quyết "
        "các vấn đề thực tế mà doanh nghiệp bán lẻ thường gặp: quản lý kho thủ công, khó đồng bộ dữ liệu "
        "giữa các chi nhánh, thiếu báo cáo kinh doanh theo thời gian thực và phân quyền nhân sự chưa rõ ràng.",
        indent=True,
    )
    add_body(doc, "Các mục tiêu cụ thể bao gồm:", indent=True)
    objectives = [
        "Nghiên cứu tổng quan về hệ thống POS và mô hình vận hành chuỗi cửa hàng bán lẻ đa chi nhánh.",
        "Phân tích, thiết kế và triển khai hệ thống web đáp ứng đầy đủ nghiệp vụ cho nhiều vai trò người dùng "
        "(Super Admin, Store Admin, Branch Manager, Cashier).",
        "Xây dựng luồng bán hàng tại quầy chuyên nghiệp: quản lý ca làm việc, tạo đơn hàng, thanh toán đa hình thức, "
        "hoàn trả và đối soát doanh thu cuối ca.",
        "Phát triển module báo cáo, thống kê trực quan giúp các cấp quản lý theo dõi và điều phối hoạt động kinh doanh "
        "trên toàn chuỗi theo thời gian thực.",
        "Áp dụng kiến trúc phân tầng, REST API kết hợp SPA, xác thực JWT và phân quyền RBAC nhằm đảm bảo tính bảo mật, "
        "mở rộng và dễ bảo trì.",
    ]
    for obj in objectives:
        add_bullet(doc, obj)

    # ===== 4. GIỚI HẠN VÀ PHẠM VI =====
    add_heading(doc, "4. GIỚI HẠN VÀ PHẠM VI CỦA ĐỀ TÀI", level=2)
    add_body(doc, "Phạm vi thực hiện:", indent=True, bold=True)
    scope_items = [
        "Phát triển ứng dụng web gồm backend (Spring Boot) và frontend (React + Vite), triển khai trên môi trường "
        "phát triển cục bộ (localhost) và có thể container hóa bằng Docker.",
        "Hỗ trợ 7 vai trò người dùng: Super Admin, Store Admin, Store Manager, Branch Manager, Branch Admin, "
        "Branch Cashier và Customer (dùng nội bộ).",
        "Các nghiệp vụ chính: đăng ký/duyệt cửa hàng, quản lý gói dịch vụ (subscription), quản lý chi nhánh, "
        "sản phẩm, danh mục, nhân viên, tồn kho, bán hàng tại quầy, ca làm việc, hoàn trả và báo cáo thống kê.",
        "Cơ sở dữ liệu quan hệ MySQL với các bảng chính: users, stores, branches, products, categories, inventories, "
        "orders, order_items, shift_report, refund, subscription_plans, subscriptions, payment.",
        "Tích hợp các dịch vụ bên ngoài: Cloudinary (lưu trữ ảnh sản phẩm), Razorpay/Stripe (thanh toán gói dịch vụ), "
        "Gmail SMTP (gửi email reset mật khẩu).",
    ]
    for item in scope_items:
        add_bullet(doc, item)

    add_body(doc, "Giới hạn của đề tài:", indent=True, bold=True)
    limits = [
        "Hệ thống tập trung vào nghiệp vụ POS cho chuỗi bán lẻ, chưa mở rộng sang thương mại điện tử (e-commerce) "
        "hoặc quản lý chuỗi cung ứng phức tạp.",
        "Thanh toán tại quầy hỗ trợ tiền mặt (CASH), thẻ (CARD) và UPI; chưa tích hợp đầy đủ các cổng thanh toán "
        "nội địa Việt Nam (VNPay, MoMo...).",
        "Chưa triển khai production trên cloud với khả năng chịu tải lớn; kiểm thử chủ yếu ở mức chức năng và luồng nghiệp vụ.",
        "Ứng dụng mobile native (Android/iOS) chưa được phát triển; giao diện tối ưu cho trình duyệt web trên máy tính "
        "và máy POS cảm ứng.",
    ]
    for item in limits:
        add_bullet(doc, item)

    # ===== 5. NỘI DUNG THỰC HIỆN =====
    add_heading(doc, "5. NỘI DUNG THỰC HIỆN", level=2)

    add_body(doc, "5.1. Khảo sát và phân tích yêu cầu", bold=True)
    add_body(
        doc,
        "Tiến hành khảo sát nhu cầu quản lý bán hàng của chuỗi cửa hàng bán lẻ, phân tích các khó khăn của "
        "phương thức quản lý truyền thống. Xác định các tác nhân (Actor) và chức năng theo từng vai trò, xây dựng "
        "Use Case Diagram, Activity Diagram và Sequence Diagram cho các luồng chính: đăng nhập, tạo đơn hàng, "
        "bắt đầu/kết thúc ca, hoàn trả đơn hàng.",
        indent=True,
    )

    add_body(doc, "5.2. Thiết kế hệ thống và cơ sở dữ liệu", bold=True)
    add_body(
        doc,
        "Thiết kế kiến trúc Client–Server với mô hình multi-tenant: nhiều cửa hàng hoạt động độc lập trên cùng "
        "một nền tảng, dữ liệu được phân tách logic qua store_id và branch_id. Backend áp dụng kiến trúc phân tầng "
        "(Controller – Service – Repository – Entity/DTO), frontend là Single Page Application (SPA) với React Router "
        "điều hướng theo vai trò người dùng.",
        indent=True,
    )
    add_body(
        doc,
        "Thiết kế cơ sở dữ liệu quan hệ với sơ đồ ERD mô tả quan hệ giữa cửa hàng, chi nhánh, sản phẩm, tồn kho, "
        "đơn hàng, ca làm việc và gói dịch vụ. Mỗi chi nhánh có bản ghi tồn kho riêng cho từng sản phẩm; đơn hàng "
        "liên kết với thu ngân, chi nhánh và khách hàng (tùy chọn).",
        indent=True,
    )

    add_body(doc, "5.3. Xây dựng hệ thống xác thực và phân quyền", bold=True)
    add_body(
        doc,
        "Triển khai đăng ký, đăng nhập và xác thực bằng JWT (JSON Web Token) với Spring Security. Áp dụng RBAC "
        "(Role-Based Access Control) kết hợp lọc dữ liệu theo ngữ cảnh: API được bảo vệ bằng @PreAuthorize, "
        "Service layer truy vấn dữ liệu theo store_id/branch_id của người dùng hiện tại để đảm bảo chi nhánh A "
        "không truy cập được dữ liệu chi nhánh B. Bổ sung chức năng quên mật khẩu và reset mật khẩu qua email.",
        indent=True,
    )

    add_body(doc, "5.4. Phát triển các phân hệ chức năng", bold=True)
    modules = [
        "Phân hệ Super Admin: duyệt/chặn cửa hàng đăng ký mới, quản lý gói dịch vụ (Subscription Plans) với "
        "cấu hình giới hạn số chi nhánh, sản phẩm, nhân viên; theo dõi lịch sử thanh toán.",
        "Phân hệ Store Admin: quản lý thông tin cửa hàng, tạo/sửa/xóa chi nhánh, danh mục và sản phẩm (upload ảnh "
        "qua Cloudinary), quản lý nhân viên và phân công vai trò, đăng ký/gia hạn gói dịch vụ, xem báo cáo toàn chuỗi.",
        "Phân hệ Branch Manager: quản lý tồn kho chi nhánh, xem đơn hàng và nhân viên, báo cáo doanh thu theo ngày/tuần/tháng, "
        "top sản phẩm bán chạy và hiệu suất thu ngân.",
        "Phân hệ Cashier (Thu ngân): quản lý ca làm việc (bắt đầu/kết thúc ca), giao diện bán hàng POS với tìm kiếm sản phẩm, "
        "giỏ hàng realtime (Redux Toolkit), thuế/giảm giá, tạm giữ đơn (Hold Order), thanh toán đa hình thức, "
        "quản lý khách hàng và xử lý hoàn trả.",
    ]
    for m in modules:
        add_bullet(doc, m)

    add_body(doc, "5.5. Luồng nghiệp vụ chính của hệ thống", bold=True)
    add_body(
        doc,
        "Hệ thống vận hành theo 6 luồng nghiệp vụ cốt lõi: (1) Onboarding — đăng ký cửa hàng, Super Admin duyệt, "
        "Store Admin đăng ký gói dịch vụ; (2) Thiết lập cửa hàng — tạo chi nhánh, danh mục, sản phẩm, nhân viên; "
        "(3) Bán hàng tại quầy — thu ngân mở ca, chọn sản phẩm, tính tiền realtime, thanh toán, trừ tồn kho; "
        "(4) Tạm giữ đơn và hoàn trả — lưu/khôi phục đơn tạm, hoàn tiền và cập nhật báo cáo ca; "
        "(5) Kết ca và báo cáo — tổng hợp doanh thu, số đơn, top sản phẩm trong ca; "
        "(6) Dashboard phân tích — biểu đồ doanh thu, phân bổ thanh toán, hiệu suất thu ngân (Recharts).",
        indent=True,
    )

    add_body(doc, "5.6. Kiến trúc kỹ thuật và luồng xử lý request", bold=True)
    add_body(
        doc,
        "Hệ thống được tổ chức theo mô hình Client–Server: trình duyệt chạy React Frontend (localhost:5173) "
        "giao tiếp với Spring Boot Backend (localhost:5000) qua HTTP kèm JWT token. Backend kết nối MySQL "
        "(localhost:3306) thông qua JPA/Hibernate. Các dịch vụ bên ngoài gồm Cloudinary (upload ảnh trực tiếp "
        "từ frontend), Razorpay/Stripe (thanh toán gói subscription qua backend) và Gmail SMTP (gửi email reset mật khẩu).",
        indent=True,
    )
    add_body(
        doc,
        "Luồng xử lý request tiêu biểu: (1) Người dùng tương tác trên giao diện React; (2) Component dispatch "
        "Redux thunk; (3) Thunk gọi Axios gửi HTTP request tới backend; (4) JwtValidator filter kiểm tra token; "
        "(5) Controller nhận request và gọi Service; (6) Service xử lý business logic, gọi Repository; "
        "(7) Repository thực thi SQL trên MySQL; (8) Kết quả trả ngược qua Mapper (Entity → DTO) → JSON → Frontend; "
        "(9) Redux cập nhật state, React re-render giao diện.",
        indent=True,
    )

    add_body(doc, "5.7. Thiết kế giao diện theo vai trò", bold=True)
    add_body(
        doc,
        "Giao diện được thiết kế theo từng phân hệ tương ứng vai trò người dùng, đảm bảo mỗi nhóm chỉ thấy "
        "các chức năng phù hợp: Super Admin truy cập /super-admin/* (dashboard tổng quan, quản lý cửa hàng và gói dịch vụ); "
        "Store Admin truy cập /store/* (quản lý chi nhánh, sản phẩm, nhân viên, báo cáo toàn chuỗi); "
        "Branch Manager truy cập /branch/* (tồn kho, đơn hàng, báo cáo chi nhánh); "
        "Cashier truy cập /cashier/* (giao diện POS tối ưu tốc độ thao tác, quản lý ca, hoàn trả). "
        "Sử dụng 48 component UI từ thư viện shadcn/ui (Button, Dialog, Table, Form...) kết hợp Tailwind CSS "
        "để đảm bảo giao diện thống nhất, hiện đại và responsive.",
        indent=True,
    )

    add_body(doc, "5.8. Kiểm thử và hoàn thiện", bold=True)
    add_body(
        doc,
        "Thực hiện kiểm thử chức năng theo từng vai trò và luồng nghiệp vụ, sử dụng Postman cho API backend "
        "và kiểm thử giao diện trên trình duyệt. Kiểm tra các trường hợp biên: thu ngân chưa mở ca không được bán hàng, "
        "mở ca trùng lặp bị từ chối, hoàn trả cập nhật đúng báo cáo ca, phân quyền chặn truy cập trái phép giữa các chi nhánh. "
        "Hoàn thiện tài liệu kỹ thuật (TECHNICAL_DOCS), kịch bản demo 6 luồng nghiệp vụ và hướng dẫn triển khai "
        "môi trường phát triển (Java 17, Node.js 18+, MySQL 8.0, Docker Compose).",
        indent=True,
    )

    doc.add_page_break()

    # ===== 6. KẾT QUẢ THỰC HIỆN =====
    add_heading(doc, "6. KẾT QUẢ THỰC HIỆN", level=2)
    add_body(
        doc,
        "Sau quá trình thực hiện, đề tài đã đạt được các kết quả cụ thể sau:",
        indent=True,
    )

    results = [
        "Xây dựng thành công hệ thống POS đa chi nhánh hoàn chỉnh (Zosh POS) với backend Spring Boot 3.5.3 "
        "và frontend React 19 + Vite 7, giao tiếp qua REST API.",
        "Triển khai đầy đủ nghiệp vụ cho 4 nhóm người dùng chính: Super Admin, Store Admin/Manager, "
        "Branch Manager/Admin và Branch Cashier, với giao diện thân thiện sử dụng Tailwind CSS và shadcn/ui.",
        "Hoàn thiện luồng bán hàng tại quầy: mở ca → chọn sản phẩm → tính thuế/giảm giá → thanh toán → "
        "cập nhật tồn kho → kết ca với báo cáo tổng hợp chính xác.",
        "Xây dựng module báo cáo thống kê với biểu đồ trực quan (doanh thu theo thời gian, top sản phẩm, "
        "hiệu suất thu ngân, phân bổ phương thức thanh toán) và chức năng xuất báo cáo biểu đồ.",
        "Thiết kế cơ sở dữ liệu MySQL với hơn 15 bảng, đảm bảo tính toàn vẹn dữ liệu và hỗ trợ mô hình multi-tenant.",
        "Tích hợp bảo mật JWT, mã hóa mật khẩu BCrypt, phân quyền RBAC và validate dữ liệu đầu vào (Bean Validation, Zod/Yup).",
        "Hệ thống có khả năng container hóa bằng Docker Compose, hỗ trợ triển khai nhanh trong môi trường demo và phát triển.",
    ]
    for r in results:
        add_bullet(doc, r)

    add_body(doc, "6.1. Chi tiết các phân hệ đã triển khai", bold=True)
    subsystems = [
        ("Super Admin", "Dashboard tổng quan số cửa hàng PENDING/ACTIVE; phê duyệt/chặn cửa hàng; CRUD gói dịch vụ "
         "với giới hạn chi nhánh/sản phẩm/nhân viên; theo dõi lịch sử thanh toán subscription."),
        ("Store Admin", "Quản lý thông tin cửa hàng; CRUD chi nhánh (địa chỉ, giờ mở/đóng, ngày làm việc); "
         "CRUD danh mục và sản phẩm (SKU, giá MRP/selling price, upload ảnh Cloudinary); "
         "quản lý nhân viên và phân quyền; đăng ký/gia hạn gói; dashboard doanh thu toàn chuỗi."),
        ("Branch Manager", "Xem/cập nhật tồn kho theo chi nhánh; xem danh sách đơn hàng và chi tiết; "
         "theo dõi nhân viên và ca làm việc; báo cáo doanh thu ngày/tuần/tháng; top sản phẩm bán chạy; "
         "biểu đồ hiệu suất thu ngân."),
        ("Cashier (Thu ngân)", "Bắt đầu/kết thúc ca (mỗi thu ngân 1 ca/ngày); giao diện POS với tìm kiếm sản phẩm; "
         "giỏ hàng Redux realtime (subtotal, thuế VAT, giảm giá); tạm giữ đơn (Hold Order); "
         "thanh toán CASH/CARD/UPI; quản lý khách hàng; hoàn trả đơn hàng với lý do; tra cứu lịch sử đơn trong ca."),
    ]
    for name, desc in subsystems:
        add_body(doc, f"• {name}: {desc}", indent=True)

    add_body(doc, "6.2. Bảng tóm tắt công nghệ sử dụng", bold=True)
    tech_table = doc.add_table(rows=1, cols=3)
    tech_table.style = "Table Grid"
    hdr = tech_table.rows[0].cells
    for i, text in enumerate(["Tầng", "Công nghệ", "Vai trò"]):
        hdr[i].text = text
        for p in hdr[i].paragraphs:
            for run in p.runs:
                set_run_font(run, size=12, bold=True)

    tech_rows = [
        ("Frontend", "React 19, Vite 7, Redux Toolkit", "Giao diện SPA, quản lý state, routing"),
        ("Frontend", "Tailwind CSS, shadcn/ui, Recharts", "UI components, biểu đồ dashboard"),
        ("Backend", "Spring Boot 3.5.3, Spring Security", "REST API, xác thực & phân quyền"),
        ("Backend", "Spring Data JPA, Hibernate", "ORM, truy vấn cơ sở dữ liệu"),
        ("Database", "MySQL 8.0", "Lưu trữ dữ liệu quan hệ"),
        ("Bảo mật", "JWT (jjwt 0.12.6), BCrypt", "Xác thực token, mã hóa mật khẩu"),
        ("Tích hợp", "Cloudinary, Razorpay/Stripe, Gmail SMTP", "Ảnh, thanh toán, email"),
        ("DevOps", "Docker, Git", "Container hóa, quản lý mã nguồn"),
    ]
    for row_data in tech_rows:
        row = tech_table.add_row().cells
        for i, text in enumerate(row_data):
            row[i].text = text
            for p in row[i].paragraphs:
                for run in p.runs:
                    set_run_font(run, size=12)

    doc.add_paragraph()

    # ===== 7. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN =====
    add_heading(doc, "7. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", level=2)

    add_body(doc, "6.3. Đánh giá hiệu quả", bold=True)
    add_body(
        doc,
        "Hệ thống đáp ứng được các yêu cầu nghiệp vụ cốt lõi của chuỗi bán lẻ đa chi nhánh: từ khâu onboarding "
        "cửa hàng mới, thiết lập dữ liệu nền, vận hành bán hàng tại quầy đến báo cáo quản trị. Mô hình multi-tenant "
        "cho phép mở rộng phục vụ nhiều doanh nghiệp trên cùng hạ tầng. Kiến trúc REST API + SPA tách biệt frontend "
        "và backend, thuận lợi cho việc bảo trì và phát triển độc lập. Việc tính toán giỏ hàng tại frontend (Redux) "
        "đảm bảo trải nghiệm mượt mà cho thu ngân, trong khi backend vẫn validate giá trước khi lưu đơn hàng.",
        indent=True,
    )

    add_body(doc, "7.1. Kết luận", bold=True)
    add_body(
        doc,
        "Đề tài đã hoàn thành việc xây dựng hệ thống điểm bán hàng đa chi nhánh Zosh POS, đáp ứng các yêu cầu "
        "nghiệp vụ cốt lõi của chuỗi cửa hàng bán lẻ. Hệ thống áp dụng kiến trúc web hiện đại, phân quyền chặt chẽ "
        "theo vai trò và mô hình multi-tenant, cho phép nhiều doanh nghiệp cùng sử dụng trên một nền tảng thống nhất.",
        indent=True,
    )
    add_body(
        doc,
        "Qua quá trình thực hiện, sinh viên đã rèn luyện kỹ năng phân tích hệ thống, thiết kế cơ sở dữ liệu quan hệ, "
        "phát triển ứng dụng web full-stack theo mô hình phân tầng và tích hợp các dịch vụ bên ngoài. Luồng bán hàng "
        "tại quầy với quản lý ca làm việc, tính toán giỏ hàng realtime và báo cáo thống kê phản ánh sát thực tế vận hành "
        "của một hệ thống POS chuyên nghiệp.",
        indent=True,
    )

    add_body(doc, "7.2. Hướng phát triển", bold=True)
    future = [
        "Tích hợp các cổng thanh toán phổ biến tại Việt Nam (VNPay, MoMo, ZaloPay) cho cả thanh toán tại quầy "
        "và gia hạn gói dịch vụ.",
        "Phát triển ứng dụng mobile (React Native hoặc Flutter) cho thu ngân và quản lý chi nhánh, hỗ trợ bán hàng "
        "trên thiết bị di động và máy POS cảm ứng.",
        "Mở rộng module thương mại điện tử, đồng bộ tồn kho giữa bán online và bán tại quầy.",
        "Triển khai trên cloud (AWS, GCP hoặc Azure) với CI/CD, monitoring và auto-scaling để phục vụ production.",
        "Bổ sung tính năng AI: dự báo nhu cầu tồn kho, gợi ý sản phẩm bán chéo, chatbot hỗ trợ vận hành (đã có hướng "
        "dẫn tích hợp trong tài liệu dự án).",
        "Hỗ trợ đa ngôn ngữ, in hóa đơn nhiệt (thermal printer) và tích hợp mã vạch/quét QR sản phẩm.",
    ]
    for f in future:
        add_bullet(doc, f)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    r = p.add_run("Ngày ...... tháng ...... năm 2026\n\n")
    set_run_font(r)
    r = p.add_run("Sinh viên thực hiện\n\n")
    set_run_font(r, bold=True)
    r = p.add_run("....................................")
    set_run_font(r)

    return doc


if __name__ == "__main__":
    output = "/Users/Study/DOAN/z pos-source-code_1/TOM_TAT_DO_AN_TOT_NGHIEP.docx"
    doc = build_document()
    doc.save(output)
    print(f"Created: {output}")
