#!/usr/bin/env python3
"""Tóm tắt đồ án V3 — dễ hiểu, ít thuật ngữ IT, nhiều bảng."""

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn


def set_font(run, size=13, bold=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = bold
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")


def heading(doc, text, center=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    r = p.add_run(text)
    set_font(r, 14 if center else 13, True)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
    return p


def para(doc, text, indent=False, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        p.paragraph_format.first_line_indent = Cm(1.27)
    r = p.add_run(text)
    set_font(r, bold=bold)
    return p


def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.left_indent = Cm(1.0)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    set_font(r)
    return p


def add_table(doc, headers, rows, col_widths=None):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    for i, h in enumerate(headers):
        tbl.rows[0].cells[i].text = h
        for p in tbl.rows[0].cells[i].paragraphs:
            for r in p.runs:
                set_font(r, 12, True)
    for row_data in rows:
        row = tbl.add_row().cells
        for i, cell in enumerate(row_data):
            row[i].text = cell
            for p in row[i].paragraphs:
                for r in p.runs:
                    set_font(r, 12)
    doc.add_paragraph()
    return tbl


def build():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Cm(2.5)
        s.bottom_margin = Cm(2.5)
        s.left_margin = Cm(3.0)
        s.right_margin = Cm(2.0)

    # ===== TRANG BÌA =====
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for text, sz in [
        ("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ GTVT\n", 13),
        ("KHOA CÔNG NGHỆ THÔNG TIN\n\n", 13),
        ("TÓM TẮT ĐỒ ÁN TỐT NGHIỆP\n\n", 16),
        (
            "XÂY DỰNG HỆ THỐNG ĐIỂM BÁN HÀNG (POS)\n"
            "ĐA CHI NHÁNH CHO CHUỖI CỬA HÀNG BÁN LẺ\n\n",
            14,
        ),
    ]:
        r = t.add_run(text)
        set_font(r, sz, True)

    for label, val in [
        ("Họ và tên:", "..............................................................."),
        ("Mã sinh viên:", ".........................................................................."),
        ("Lớp:", "..........................."),
        ("Ngành:", "Công nghệ thông tin"),
        ("Giảng viên hướng dẫn:", "ThS. Phạm Văn A"),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        set_font(p.add_run(f"{label} "), bold=True)
        set_font(p.add_run(val))

    doc.add_page_break()

    # ===== 1. THÔNG TIN =====
    heading(doc, "1. THÔNG TIN SINH VIÊN")
    for line in [
        "Họ và tên: ...............................................................",
        "Mã sinh viên: ..........................................................................",
        "Lớp: ...........................  |  Ngành: Công nghệ thông tin",
        "Giảng viên hướng dẫn: ThS. Phạm Văn A",
    ]:
        para(doc, line, indent=True)

    # ===== 2. TÊN ĐỀ TÀI =====
    heading(doc, "2. TÊN ĐỀ TÀI")
    para(
        doc,
        "Xây dựng hệ thống quản lý bán hàng tại quầy (POS) đa chi nhánh cho chuỗi cửa hàng bán lẻ — "
        "tên hệ thống: Zosh POS.",
        indent=True,
    )

    # ===== 3. HỆ THỐNG LÀ GÌ? =====
    heading(doc, "3. HỆ THỐNG LÀ GÌ? — GIẢI THÍCH DỄ HIỂU")
    para(
        doc,
        "Zosh POS giống như một \"phần mềm quản lý cửa hàng trên trình duyệt web\". Một chủ chuỗi "
        "cà phê, tạp hóa hay thời trang có thể đăng ký, mở nhiều chi nhánh, thêm nhân viên, "
        "bán hàng tại quầy và xem báo cáo doanh thu — tất cả trên cùng một nền tảng.",
        indent=True,
    )
    para(
        doc,
        "Điểm khác biệt so với phần mềm bán hàng thông thường: hệ thống phục vụ nhiều doanh nghiệp "
        "cùng lúc (giống mô hình GrabFood hay Shopify), mỗi doanh nghiệp quản lý riêng dữ liệu của mình, "
        "không lẫn lộn với cửa hàng khác.",
        indent=True,
    )

    para(doc, "So sánh nhanh với cách quản lý truyền thống:", bold=True)
    add_table(
        doc,
        ["Tiêu chí", "Quản lý thủ công / Excel", "Zosh POS"],
        [
            ("Ghi đơn hàng", "Viết tay hoặc nhập Excel", "Click chọn sản phẩm, tự tính tiền"),
            ("Theo dõi nhiều chi nhánh", "Khó, dễ sai", "Một màn hình xem toàn chuỗi"),
            ("Chuyển khoản của khách", "Thu ngân kiểm tra ảnh màn hình", "Tự động nhận tiền qua QR"),
            ("Cuối ca đối soát", "Đếm tay, dễ thiếu thừa", "Hệ thống tổng kết tự động"),
            ("Xem báo cáo kinh doanh", "Tổng hợp thủ công cuối tháng", "Biểu đồ cập nhật theo thời gian thực"),
            ("Hỏi nhanh \"hôm nay bán được bao nhiêu?\"", "Phải mở sổ hoặc Excel", "Hỏi Chatbot, trả lời ngay"),
        ],
    )
    add_table(
        doc,
        ["Vấn đề thực tế", "Hệ thống giải quyết như thế nào"],
        [
            ("Ghi chép sổ sách, tính tiền tay", "Bán hàng trên máy tính, tự tính tiền, in biên lai"),
            ("Không biết chi nhánh nào bán tốt", "Báo cáo doanh thu theo từng chi nhánh, theo ngày/tuần/tháng"),
            ("Thu ngân không đối soát được cuối ca", "Tự động tổng kết doanh thu, hoàn trả khi kết ca"),
            ("Quản lý nhiều cửa hàng rối", "Một tài khoản chủ cửa hàng quản lý toàn bộ chuỗi"),
            ("Khách chuyển khoản, thu ngân phải kiểm tra tay", "Quét QR — hệ thống tự nhận tiền, tự tạo đơn"),
        ],
    )

    # ===== 4. MỤC TIÊU =====
    heading(doc, "4. MỤC TIÊU CỦA ĐỀ TÀI")
    for g in [
        "Xây dựng phần mềm quản lý bán hàng phù hợp chuỗi cửa hàng có nhiều chi nhánh.",
        "Phân quyền rõ ràng: ai được làm gì — từ quản trị viên hệ thống đến thu ngân.",
        "Hỗ trợ bán hàng nhanh tại quầy: chọn món, tính tiền, thanh toán, in hóa đơn.",
        "Tự động hóa thanh toán chuyển khoản QR — không cần thu ngân xác nhận tay.",
        "Cung cấp báo cáo kinh doanh trực quan và trợ lý AI trả lời câu hỏi bằng tiếng Việt.",
    ]:
        bullet(doc, g)

    # ===== 5. PHÂN CẤP QUẢN LÝ =====
    heading(doc, "5. MÔ HÌNH PHÂN CẤP QUẢN LÝ ĐA TẦNG")
    para(
        doc,
        "Hệ thống có 4 cấp quản lý xếp từ trên xuống dưới. Mỗi cấp chỉ thấy và thao tác đúng phần "
        "việc của mình — giống cơ cấu tổ chức thực tế của một chuỗi bán lẻ.",
        indent=True,
    )

    add_table(
        doc,
        ["Cấp", "Ai sử dụng?", "Làm được gì?", "Không được làm gì?"],
        [
            (
                "Cấp 1\nQuản trị hệ thống",
                "Super Admin",
                "Duyệt cửa hàng mới đăng ký; quản lý gói dịch vụ; giám sát toàn bộ hệ thống",
                "Không bán hàng, không can thiệp chi tiết từng đơn hàng",
            ),
            (
                "Cấp 2\nChủ cửa hàng",
                "Store Admin",
                "Tạo chi nhánh; thêm sản phẩm, nhân viên; xem báo cáo toàn chuỗi; đăng ký gói dịch vụ",
                "Không thao tác bán hàng tại quầy",
            ),
            (
                "Cấp 3\nQuản lý chi nhánh",
                "Branch Manager",
                "Xem đơn hàng, tồn kho, nhân viên tại chi nhánh mình; báo cáo doanh thu chi nhánh",
                "Không thấy dữ liệu chi nhánh khác",
            ),
            (
                "Cấp 4\nThu ngân",
                "Cashier",
                "Mở ca, bán hàng, thanh toán, hoàn trả, kết ca",
                "Không sửa giá, không thêm sản phẩm, không xem báo cáo toàn chuỗi",
            ),
        ],
    )

    para(
        doc,
        "Độ phức tạp nổi bật: dù nhiều cửa hàng và chi nhánh cùng dùng chung một hệ thống, "
        "dữ liệu của chi nhánh A hoàn toàn tách biệt với chi nhánh B. Thu ngân chỉ thấy đơn hàng "
        "của chi nhánh mình — đảm bảo bảo mật và đúng nghiệp vụ thực tế.",
        indent=True,
    )

    doc.add_page_break()

    # ===== 6. CHỨC NĂNG CHÍNH =====
    heading(doc, "6. CÁC NHÓM CHỨC NĂNG CHÍNH")

    add_table(
        doc,
        ["Nhóm chức năng", "Mô tả ngắn gọn", "Ai dùng?"],
        [
            ("Đăng ký & duyệt cửa hàng", "Doanh nghiệp đăng ký → chờ duyệt → được phép hoạt động", "Chủ cửa hàng, Super Admin"),
            ("Gói dịch vụ (Subscription)", "Chọn gói (giới hạn chi nhánh, sản phẩm, nhân viên), thanh toán online", "Chủ cửa hàng"),
            ("Quản lý chi nhánh", "Thêm/sửa chi nhánh, địa chỉ, giờ mở cửa", "Chủ cửa hàng"),
            ("Quản lý sản phẩm", "Danh mục, tên, giá, hình ảnh, mã sản phẩm", "Chủ cửa hàng"),
            ("Quản lý nhân viên", "Thêm nhân viên, gán chi nhánh, phân vai trò", "Chủ cửa hàng"),
            ("Quản lý tồn kho", "Theo dõi số lượng hàng tại từng chi nhánh", "Quản lý chi nhánh"),
            ("Bán hàng tại quầy (POS)", "Chọn hàng, tính tiền, thuế, giảm giá, thanh toán", "Thu ngân"),
            ("Quản lý ca làm việc", "Mở ca, bán hàng trong ca, kết ca và in báo cáo", "Thu ngân"),
            ("Hoàn trả hàng", "Tìm đơn cũ, nhập lý do, hoàn tiền", "Thu ngân"),
            ("Tạm giữ đơn", "Lưu đơn chưa thanh toán, phục vụ khách khác trước", "Thu ngân"),
            ("Báo cáo & biểu đồ", "Doanh thu, sản phẩm bán chạy, hiệu suất thu ngân", "Chủ cửa hàng, Quản lý CN"),
            ("Trợ lý AI Chatbot", "Hỏi bằng tiếng Việt, nhận phân tích từ dữ liệu thật", "Tất cả người dùng"),
        ],
    )

    para(doc, "Các gói dịch vụ — giới hạn theo gói đăng ký:", bold=True)
    add_table(
        doc,
        ["Nội dung gói", "Ví dụ Starter", "Ví dụ Pro"],
        [
            ("Số chi nhánh tối đa", "1–2 chi nhánh", "5–10 chi nhánh"),
            ("Số sản phẩm tối đa", "50 sản phẩm", "500 sản phẩm"),
            ("Số nhân viên tối đa", "5 người", "20 người"),
            ("Báo cáo nâng cao", "Cơ bản", "Đầy đủ + xuất PDF"),
            ("Thanh toán gói", "Theo tháng / theo năm qua cổng online", "Theo tháng / theo năm qua cổng online"),
        ],
    )

    # ===== 7. LUỒNG NGHIỆP VỤ =====
    heading(doc, "7. LUỒNG NGHIỆP VỤ CHÍNH — KỂ BẰNG LỜI THƯỜNG")

    flows = [
        (
            "Luồng 1: Một cửa hàng mới tham gia hệ thống",
            [
                "Chủ cửa hàng đăng ký tài khoản trên website.",
                "Điền thông tin cửa hàng (tên, địa chỉ, loại hình).",
                "Hệ thống chuyển trạng thái \"Chờ duyệt\".",
                "Quản trị viên hệ thống xem và bấm \"Duyệt\".",
                "Chủ cửa hàng chọn gói dịch vụ và thanh toán online.",
                "Cửa hàng chính thức hoạt động.",
            ],
        ),
        (
            "Luồng 2: Chuẩn bị trước khi bán hàng",
            [
                "Chủ cửa hàng tạo các chi nhánh (VD: Quận 1, Quận 3).",
                "Thêm danh mục và sản phẩm (cà phê, trà, bánh... kèm giá và hình ảnh).",
                "Thêm nhân viên: gán ai là quản lý chi nhánh, ai là thu ngân.",
                "Nhập số lượng tồn kho ban đầu cho từng chi nhánh.",
            ],
        ),
        (
            "Luồng 3: Một ca bán hàng điển hình (quan trọng nhất)",
            [
                "Thu ngân đăng nhập → bấm \"Bắt đầu ca\" (hệ thống ghi nhận giờ mở ca).",
                "Khách chọn món → thu ngân click thêm vào đơn → tiền tự tính ngay trên màn hình.",
                "Có thể thêm thuế, giảm giá; có thể tạm giữ đơn nếu khách chưa trả tiền.",
                "Khách thanh toán (tiền mặt / thẻ / quét QR).",
                "Hệ thống tạo hóa đơn, cập nhật tồn kho.",
                "Cuối ca: bấm \"Kết thúc ca\" → nhận báo cáo tổng doanh thu, số đơn, tiền hoàn trả.",
            ],
        ),
        (
            "Luồng 4: Xử lý hoàn trả",
            [
                "Khách mang hàng quay lại đổi/hoàn.",
                "Thu ngân tìm đơn hàng cũ trong hệ thống.",
                "Nhập lý do hoàn trả → xác nhận.",
                "Đơn chuyển sang trạng thái \"Đã hoàn\" — số tiền được trừ vào báo cáo ca.",
            ],
        ),
        (
            "Luồng 5: Chủ cửa hàng xem báo cáo",
            [
                "Vào trang Dashboard → xem biểu đồ doanh thu 7 ngày.",
                "Xem sản phẩm bán chạy nhất, thu ngân bán giỏi nhất.",
                "So sánh doanh thu giữa các chi nhánh.",
                "Có thể xuất báo cáo ra file PDF.",
            ],
        ),
    ]

    for title, steps in flows:
        para(doc, title, bold=True)
        for i, step in enumerate(steps, 1):
            bullet(doc, f"Bước {i}: {step}")
        doc.add_paragraph()

    doc.add_page_break()

    # ===== 8. THANH TOÁN =====
    heading(doc, "8. HỆ THỐNG THANH TOÁN — ĐIỂM NỔI BẬT CỦA ĐỒ ÁN")

    para(
        doc,
        "Hệ thống hỗ trợ 3 cách khách trả tiền tại quầy, và 1 cách chủ cửa hàng trả phí dịch vụ hàng tháng.",
        indent=True,
    )

    add_table(
        doc,
        ["Hình thức", "Cách hoạt động", "Mức độ tự động"],
        [
            (
                "Tiền mặt",
                "Thu ngân nhập số tiền khách đưa → hệ thống tính tiền thối → xác nhận",
                "Tự động tính tiền thối",
            ),
            (
                "Thẻ ngân hàng",
                "Khách quẹt thẻ trên máy POS vật lý → thu ngân xác nhận đã nhận tiền",
                "Xác nhận thủ công",
            ),
            (
                "Quét QR chuyển khoản",
                "Khách quét mã QR → chuyển khoản → hệ thống TỰ phát hiện tiền về → TỰ tạo đơn hàng",
                "Tự động 100%",
            ),
            (
                "Thanh toán gói dịch vụ",
                "Chủ cửa hàng chọn gói → thanh toán online qua cổng quốc tế → kích hoạt gói",
                "Tự động sau khi thanh toán",
            ),
        ],
    )

    para(doc, "Thanh toán QR — tại sao đây là điểm hay nhất?", bold=True)
    para(
        doc,
        "Ở nhiều cửa hàng nhỏ, khách chuyển khoản xong phải đưa ảnh màn hình cho thu ngân kiểm tra — "
        "chậm và dễ nhầm. Zosh POS giải quyết triệt để:",
        indent=True,
    )
    for s in [
        "Khi khách chọn \"Chuyển khoản QR\", màn hình hiện mã QR đã ghi sẵn số tiền và mã đơn hàng.",
        "Khách quét bằng app ngân hàng và chuyển tiền.",
        "Hệ thống liên tục kiểm tra tài khoản ngân hàng (qua dịch vụ SePay) — khoảng vài giây một lần.",
        "Khi phát hiện đúng số tiền và đúng mã đơn → tự động xác nhận, tạo hóa đơn, in biên lai.",
        "Thu ngân KHÔNG cần bấm xác nhận tay — giảm sai sót, tăng tốc phục vụ khách.",
    ]:
        bullet(doc, s)

    para(
        doc,
        "Độ phức tạp: phải đồng bộ giữa 3 bên (màn hình thu ngân, ngân hàng khách chuyển, máy chủ hệ thống), "
        "xử lý trường hợp nhiều khách thanh toán cùng lúc, và đảm bảo không nhận nhầm giao dịch của người khác.",
        indent=True,
    )

    para(doc, "Ví dụ tình huống thực tế — khách quét QR:", bold=True)
    add_table(
        doc,
        ["Thời điểm", "Chuyện gì xảy ra?"],
        [
            ("0 giây", "Thu ngân bấm \"Chuyển khoản QR\" — màn hình hiện mã QR và số tiền"),
            ("5 giây", "Khách mở app ngân hàng, quét QR, bấm chuyển tiền"),
            ("10–15 giây", "Ngân hàng ghi nhận giao dịch"),
            ("15–20 giây", "Hệ thống phát hiện tiền đã về, khớp đúng số tiền và mã đơn"),
            ("20 giây", "Tự động tạo hóa đơn, hiện thông báo thành công — thu ngân không cần làm gì thêm"),
        ],
    )

    # ===== 9. AI CHATBOT =====
    heading(doc, "9. TRỢ LÝ AI CHATBOT — HỎI BẰNG TIẾNG VIỆT, TRẢ LỜI TỪ DỮ LIỆU THẬT")

    para(
        doc,
        "Góc phải màn hình có biểu tượng trợ lý AI. Người dùng gõ câu hỏi bình thường — "
        "không cần biết cách xem báo cáo hay thao tác phức tạp.",
        indent=True,
    )

    add_table(
        doc,
        ["Bạn có thể hỏi...", "AI trả lời dựa trên..."],
        [
            ("\"Doanh thu hôm nay bao nhiêu?\"", "Tổng đơn hàng và tiền thu được trong ngày"),
            ("\"Sản phẩm nào bán chạy nhất?\"", "Thống kê số lượng bán thực tế"),
            ("\"Chi nhánh nào doanh thu cao nhất?\"", "So sánh doanh thu từng chi nhánh"),
            ("\"Có hàng nào sắp hết không?\"", "Danh sách sản phẩm tồn kho thấp"),
            ("\"So sánh hôm nay với hôm qua\"", "Doanh thu 2 ngày + % tăng/giảm"),
        ],
    )

    # ===== 3b. GIỚI HẠN =====
    heading(doc, "3.1. Giới hạn và phạm vi thực hiện")
    add_table(
        doc,
        ["Trong phạm vi đồ án", "Ngoài phạm vi (hướng mở rộng sau)"],
        [
            ("Quản lý bán hàng tại quầy cho chuỗi cửa hàng", "Bán hàng online / giao hàng"),
            ("3 hình thức thanh toán tại quầy + thanh toán gói dịch vụ", "Tích hợp MoMo, VNPay tại quầy"),
            ("Báo cáo, biểu đồ, Chatbot AI", "Ứng dụng điện thoại riêng"),
            ("Chạy trên máy tính qua trình duyệt web", "Triển khai quy mô lớn trên cloud"),
        ],
    )

    add_table(
        doc,
        ["Tính năng", "Giải thích"],
        [
            ("Chat tiếng Việt tự nhiên", "Gõ như nhắn tin, không cần thuật ngữ kỹ thuật"),
            ("Dữ liệu thật, không bịa", "AI đọc số liệu từ hệ thống rồi mới trả lời — không đoán mò"),
            ("Phân quyền thông minh", "Chủ cửa hàng thấy toàn chuỗi; quản lý chi nhánh chỉ thấy chi nhánh mình"),
            ("Phân tích nhanh 1 click", "Nút \"Insight\" — AI tự tóm tắt tình hình kinh doanh"),
            ("Gợi ý câu hỏi", "8 câu hỏi mẫu, bấm là hỏi ngay"),
        ],
    )

    para(
        doc,
        "Độ phức tạp: kết hợp trí tuệ nhân tạo (Google Gemini) với dữ liệu bán hàng thực, "
        "đảm bảo mỗi người chỉ được xem đúng phần dữ liệu của mình — vừa tiện lợi vừa an toàn.",
        indent=True,
    )

    doc.add_page_break()

    # ===== 10. ĐIỂM HAY & PHỨC TẠP =====
    heading(doc, "10. NHỮNG ĐIỂM HAY VÀ ĐỘ PHỨC TẠP NỔI BẬT")

    add_table(
        doc,
        ["Điểm nổi bật", "Giải thích dễ hiểu", "Tại sao quan trọng?"],
        [
            (
                "Quản lý đa tầng",
                "4 cấp từ Super Admin → Thu ngân, mỗi cấp một quyền hạn",
                "Phản ánh đúng cơ cấu chuỗi bán lẻ thực tế",
            ),
            (
                "Nhiều cửa hàng, một nền tảng",
                "Giống mô hình SaaS — nhiều doanh nghiệp dùng chung, dữ liệu tách biệt",
                "Có thể mở rộng kinh doanh phần mềm",
            ),
            (
                "Thanh toán QR tự động 100%",
                "Khách quét QR → hệ thống tự nhận tiền → tự tạo đơn",
                "Giảm sai sót, tăng tốc phục vụ — ít phần mềm POS sinh viên làm được",
            ),
            (
                "Quản lý ca làm việc",
                "Bắt buộc mở ca mới bán; kết ca tự tổng kết doanh thu",
                "Minh bạch tiền mặt, chống gian lận thu ngân",
            ),
            (
                "Tính tiền tức thì",
                "Thêm/bớt món, giảm giá — tiền nhảy ngay trên màn hình",
                "Thu ngân không phải chờ, phục vụ nhanh hơn",
            ),
            (
                "Tạm giữ đơn hàng",
                "Lưu đơn chưa trả, phục vụ khách khác, quay lại đơn cũ sau",
                "Giải quyết tình huống thực tế tại quầy",
            ),
            (
                "AI Chatbot tiếng Việt",
                "Hỏi đáp kinh doanh bằng lời nói thường",
                "Điểm cộng lớn, vượt POS truyền thống",
            ),
            (
                "Báo cáo trực quan",
                "Biểu đồ doanh thu, top sản phẩm, xuất PDF",
                "Chủ cửa hàng ra quyết định nhanh hơn",
            ),
        ],
    )

    # ===== 11. KẾT QUẢ =====
    heading(doc, "11. KẾT QUẢ ĐẠT ĐƯỢC")

    add_table(
        doc,
        ["Hạng mục", "Kết quả"],
        [
            ("Phần mềm hoàn chỉnh", "Website quản lý bán hàng chạy được trên trình duyệt"),
            ("Số vai trò người dùng", "4 nhóm chính: Quản trị hệ thống, Chủ cửa hàng, Quản lý chi nhánh, Thu ngân"),
            ("Thanh toán", "Tiền mặt + Thẻ + QR tự động + Thanh toán gói dịch vụ online"),
            ("Trợ lý AI", "Chatbot tiếng Việt, phân tích doanh thu và tồn kho"),
            ("Báo cáo", "Dashboard biểu đồ, xuất PDF"),
            ("Triển khai", "Chạy được trên máy cá nhân, có thể đóng gói bằng Docker"),
        ],
    )

    # ===== 12. KẾT LUẬN =====
    heading(doc, "12. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    para(
        doc,
        "Đồ án đã xây dựng thành công hệ thống quản lý bán hàng đa chi nhánh Zosh POS — "
        "một giải pháp thực tế cho chuỗi cửa hàng bán lẻ. Hệ thống không chỉ \"bán hàng và in hóa đơn\" "
        "mà còn giải quyết bài toán quản lý phân cấp, đối soát ca làm việc, thanh toán tự động và "
        "hỗ trợ ra quyết định bằng AI.",
        indent=True,
    )

    para(doc, "Hướng phát triển trong tương lai:", bold=True)
    for h in [
        "Ứng dụng điện thoại cho thu ngân và quản lý.",
        "Tích hợp thêm ví điện tử Việt Nam (MoMo, VNPay).",
        "Bán hàng online, đồng bộ kho giữa web và quầy.",
        "Triển khai lên máy chủ cloud để nhiều cửa hàng dùng thật.",
    ]:
        bullet(doc, h)

    para(doc, "Gợi ý trình bày trước hội đồng (demo):", bold=True)
    add_table(
        doc,
        ["Thứ tự", "Nên demo gì?", "Vì sao ấn tượng?"],
        [
            ("1", "Mở Chatbot, hỏi \"Doanh thu hôm nay?\"", "Thể hiện AI + dữ liệu thật, dễ hiểu ngay"),
            ("2", "Thu ngân bán hàng, khách trả bằng QR", "Thanh toán tự động 100% — điểm mạnh nhất"),
            ("3", "Kết ca — xem báo cáo tổng kết", "Minh bạch quản lý tiền mặt"),
            ("4", "Chủ cửa hàng xem Dashboard biểu đồ", "Quản lý chuỗi trực quan"),
            ("5", "Super Admin duyệt cửa hàng mới", "Mô hình nhiều doanh nghiệp trên một nền tảng"),
        ],
    )

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    set_font(p.add_run("Ngày ...... tháng ...... năm 2026\n\n"), bold=False)
    set_font(p.add_run("Sinh viên thực hiện\n\n"), bold=True)
    set_font(p.add_run("...................................."))

    return doc


if __name__ == "__main__":
    path = "/Users/Study/DOAN/z pos-source-code_1/TOM_TAT_DO_AN_DE_HIEU.docx"
    build().save(path)
    print(f"Created: {path}")
