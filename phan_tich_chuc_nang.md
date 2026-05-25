# 🔍 Phân Tích Chức Năng Dự Án Zosh POS — Cái Gì Có, Cái Gì Thiếu

---

## 1. Chức Năng Hiện Có (Đã Code)

### ✅ Module Thu Ngân (Cashier)
| Chức năng | Trạng thái | Ghi chú |
|-----------|-----------|---------|
| Tạo đơn hàng (POS) | ✅ Hoàn chỉnh | 3-column layout: Sản phẩm → Giỏ hàng → Thanh toán |
| Tìm kiếm sản phẩm | ✅ Có | LIKE query đơn giản |
| Giỏ hàng (Cart) | ✅ Có | Redux state, hold orders |
| Thanh toán (Cash/Card/UPI) | ✅ Có | PaymentDialog |
| In hóa đơn | ✅ Có | InvoiceDialog |
| Lịch sử đơn hàng | ✅ Có | OrderHistoryPage + filter |
| Hoàn trả (Refund) | ✅ Có | ReturnOrderPage |
| Quản lý ca (Shift) | ✅ Có | ShiftSummary, start/end ca |
| Giảm giá (Discount) | ⚠️ Frontend only | Chỉ có UI, **chưa lưu vào DB** (Order entity không có trường discount) |
| Ghi chú đơn hàng | ⚠️ Frontend only | NoteSection có UI nhưng Order entity không có trường note |
| Quản lý khách hàng | ✅ Có | CustomerDialog, tìm kiếm |

### ✅ Module Chủ Cửa Hàng (Store Admin)
| Chức năng | Trạng thái | Ghi chú |
|-----------|-----------|---------|
| Dashboard tổng quan | ✅ Có | KPI cards, biểu đồ |
| Quản lý sản phẩm (CRUD) | ✅ Có | Thêm/sửa/xóa, upload ảnh Cloudinary |
| Quản lý danh mục | ✅ Có | CategoryController |
| Quản lý chi nhánh | ✅ Có | Thêm/sửa/xóa chi nhánh |
| Quản lý nhân viên | ✅ Có | Thêm/sửa/xóa, phân quyền |
| Biểu đồ doanh thu | ✅ Có | Theo ngày, tháng, danh mục, chi nhánh |
| Cảnh báo (Alerts) | ✅ Có | Hết hàng, không có đơn, hoàn trả, nhân viên inactive |
| Cài đặt cửa hàng | ⚠️ Chỉ UI | Settings.jsx dùng local state, **chưa lưu vào DB** |

### ✅ Module Quản Lý Chi Nhánh (Branch Manager)
| Chức năng | Trạng thái | Ghi chú |
|-----------|-----------|---------|
| Dashboard chi nhánh | ✅ Có | BranchAnalyticsController |
| Xem đơn hàng | ✅ Có | Orders page |
| Quản lý tồn kho | ✅ Có | Inventory CRUD |
| Xem khách hàng | ✅ Có | Customers page |
| Báo cáo chi nhánh | ✅ Có | Reports page |
| Giao dịch | ✅ Có | Transactions page |

### ✅ Module Super Admin
| Chức năng | Trạng thái | Ghi chú |
|-----------|-----------|---------|
| Dashboard tổng | ✅ Có | AdminDashboardController |
| Duyệt cửa hàng | ✅ Có | PENDING → ACTIVE/BLOCKED |
| Quản lý gói subscription | ✅ Có | CRUD subscription plans |
| Commissions | ⚠️ Chỉ UI | CommissionsPage.jsx — có UI nhưng chưa có backend logic |
| Exports | ⚠️ Chỉ UI | ExportsPage.jsx — có UI nhưng chưa có backend logic |

### ✅ Hệ Thống Chung
| Chức năng | Trạng thái |
|-----------|-----------|
| Đăng ký / Đăng nhập (JWT) | ✅ Có |
| Phân quyền 7 roles | ✅ Có |
| Reset mật khẩu (email) | ✅ Có |
| Thanh toán subscription (Razorpay/Stripe) | ✅ Có |
| Upload ảnh (Cloudinary) | ✅ Có |
| Docker deployment | ✅ Có |

---

## 2. ❌ Chức Năng THIẾU — Cần Làm Thêm

### 🔴 Mức Quan Trọng Cao (Thiếu = Không Thực Tế)

| # | Chức năng thiếu | Vấn đề | Mức độ khó |
|---|----------------|--------|-----------|
| 1 | **Trừ tồn kho khi bán** | `createOrder()` không trừ `inventory.quantity`. Bán hàng xong tồn kho không giảm! | ⭐ Dễ |
| 2 | **Discount không lưu DB** | Order entity không có trường `discount`. Frontend có UI nhưng backend bỏ qua | ⭐ Dễ |
| 3 | **Note đơn hàng không lưu** | NoteSection có UI nhưng Order entity không có trường `note` | ⭐ Dễ |
| 4 | **Filter order theo status bị comment** | `OrderServiceImpl` dòng 101-102: filter theo status đang bị comment out | ⭐ Dễ |
| 5 | **Settings không lưu DB** | Settings.jsx dùng `useState` hardcode, không gọi API lưu | ⭐⭐ TB |
| 6 | **Không có xuất báo cáo (Export)** | Không export Excel/PDF cho báo cáo doanh thu, tồn kho | ⭐⭐ TB |

### 🟡 Mức Quan Trọng Trung Bình (Có thì tốt hơn)

| # | Chức năng thiếu | Lý do nên thêm | Mức độ khó |
|---|----------------|----------------|-----------|
| 7 | **Barcode / QR Code** | Hệ thống POS thực tế luôn có quét mã vạch | ⭐⭐ TB |
| 8 | **In hóa đơn nhiệt (Thermal receipt)** | POS thực tế cần kết nối máy in | ⭐⭐⭐ Khó |
| 9 | **Quản lý nhà cung cấp (Supplier)** | Quản lý đầy đủ cần biết hàng nhập từ đâu | ⭐⭐ TB |
| 10 | **Nhập hàng (Purchase Order)** | Tồn kho hiện tại chỉ set thủ công, không có luồng nhập hàng | ⭐⭐ TB |
| 11 | **Lịch sử chỉnh sửa (Audit Log)** | Ai sửa gì, lúc nào — quan trọng cho quản lý | ⭐⭐ TB |
| 12 | **Thông báo realtime** | WebSocket cho: đơn mới, hết hàng, ca mới | ⭐⭐⭐ Khó |

---

## 3. 🤖 Gợi Ý Tính Năng AI — Phù Hợp & Thực Tế

> [!IMPORTANT]
> Dựa trên phân tích source code thực tế, đây là **5 tính năng AI khả thi nhất** xếp theo **ROI** (giá trị mang lại / công sức bỏ ra).

### 🏆 TOP 3 — Nên Làm Nhất

#### 1. 💬 AI Chatbot Trợ Lý Quản Lý (⭐ Dễ, 1-2 ngày)
**Tại sao thực tế?** Store Admin/Branch Manager thường cần tra cứu nhanh mà không muốn click qua nhiều trang.

**Ví dụ hỏi:**
- *"Chi nhánh nào bán chạy nhất tuần này?"*
- *"Sản phẩm nào sắp hết hàng?"*
- *"Doanh thu hôm nay so với hôm qua?"*

**Cách làm:** Lấy dữ liệu từ `StoreAnalyticsService` (đã có sẵn) → truyền vào Gemini API → trả lời bằng ngôn ngữ tự nhiên.

---

#### 2. 📊 AI Tóm Tắt Dashboard (⭐ Dễ, 1 ngày)
**Tại sao thực tế?** Dashboard hiện tại chỉ có số liệu khô. Thêm 1 card "AI Insight" tự động nhận xét xu hướng.

**Ví dụ output:**
> *"📈 Doanh thu hôm nay đạt 15.2M, tăng 23% so với hôm qua. Chi nhánh Q3 vẫn chưa có đơn hàng nào — nên kiểm tra. Sản phẩm Cà Phê Sữa bán chạy nhất (47 đơn)."*

**Cách làm:** Dùng `StoreOverviewDTO` + `BranchSalesDTO` đã có → gửi Gemini tóm tắt.

---

#### 3. 📦 Dự Đoán Tồn Kho & Gợi Ý Nhập Hàng (⭐⭐ TB, 2 ngày)
**Tại sao thực tế?** Hệ thống đã có `Alerts` cho low stock, nhưng chỉ cảnh báo khi đã thấp. AI có thể **dự đoán trước**.

**Cách làm:**
```
Trung bình bán/ngày = SUM(order_items.quantity) trong 30 ngày / 30
Số ngày còn hàng  = inventory.quantity / trung bình bán/ngày
→ Nếu < 7 ngày → "Nên nhập thêm 50 cái trong 3 ngày tới"
```

---

### 🥈 TOP 2 — Tùy Chọn Thêm

#### 4. 🔍 Tìm Kiếm Sản Phẩm Thông Minh (⭐ Dễ, 0.5 ngày)
**Hiện tại:** `searchByKeyword` chỉ dùng LIKE query đơn giản.
**Cải tiến:** Tìm gần đúng, hiểu ngữ cảnh (*"nước ngọt giá rẻ"* → lọc category đồ uống + sort giá thấp).

#### 5. ⚠️ AI Phát Hiện Giao Dịch Bất Thường (⭐⭐ TB, 1-2 ngày)
**Hiện tại:** `StoreAlertDTO` đã có refundSpikeAlerts — nhưng logic đơn giản.
**Cải tiến:** AI phân tích pattern: hoàn trả liên tục từ 1 thu ngân, đơn hàng giá trị quá lớn bất thường.

---

## 4. 📋 Khuyến Nghị Ưu Tiên

> [!TIP]
> **Cho đồ án tốt nghiệp**, tôi khuyên ưu tiên theo thứ tự:

### Bước 1: Sửa bug/thiếu quan trọng (0.5 ngày)
- ✅ Thêm **trừ tồn kho** khi tạo đơn (`OrderServiceImpl.createOrder`)
- ✅ Uncomment **filter order theo status**

### Bước 2: Thêm AI (2-3 ngày)
- 🤖 **AI Chatbot** — nổi bật nhất khi demo
- 🤖 **AI Dashboard Insight** — dễ làm, visual đẹp

### Bước 3: Hoàn thiện thêm (tùy thời gian)
- Thêm trường `discount`, `note` vào Order entity
- Export báo cáo PDF/Excel
- Barcode scan

---

Bạn muốn tôi **bắt tay làm** cái nào trước?
