# 💳 Tài liệu Hệ thống Thanh toán — POS System

> **Mục đích:** Tài liệu này giải thích toàn bộ luồng thanh toán trong hệ thống POS,  
> từ kiến trúc kỹ thuật đến cách trả lời phỏng vấn đồ án.

---

## 📋 Mục lục

1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [3 phương thức thanh toán](#2-3-phương-thức-thanh-toán)
3. [Luồng thanh toán QR — Chi tiết kỹ thuật](#3-luồng-thanh-toán-qr--chi-tiết-kỹ-thuật)
4. [Kiến trúc SePay Polling](#4-kiến-trúc-sepay-polling)
5. [Cấu trúc code](#5-cấu-trúc-code)
6. [Cấu hình hệ thống](#6-cấu-hình-hệ-thống)
7. [Câu hỏi phỏng vấn thường gặp](#7-câu-hỏi-phỏng-vấn-thường-gặp)

---

## 1. Tổng quan hệ thống

### Công nghệ sử dụng

| Layer | Technology |
|-------|-----------|
| **Frontend** | React + Vite, Redux Toolkit, Axios |
| **Backend** | Spring Boot (Java), Spring Security, Spring Scheduling |
| **Cổng thanh toán** | SePay (tích hợp ngân hàng MBBank) |
| **QR Standard** | VietQR / SePay QR |
| **Database** | MySQL |

### Sơ đồ tổng thể

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────┐
│   Cashier (FE)  │ ──────▶ │  Backend (BE)    │ ──────▶ │  Database    │
│   React/Vite    │ ◀────── │  Spring Boot     │         │  MySQL       │
└─────────────────┘         └──────────────────┘         └──────────────┘
         │                           │
         │ Poll 3s                   │ Poll 4s
         ▼                           ▼
  /api/qr-payments/           SePay API
     status/{ref}        (my.sepay.vn/userapi)
```

---

## 2. 3 phương thức thanh toán

### 2.1 💵 Tiền mặt (CASH)

**Luồng:**
```
Cashier nhập số tiền khách đưa
        ↓
Hệ thống tính tiền thối (cashAmount - total)
        ↓
Cashier bấm "Xác nhận & In biên lai"
        ↓
Backend tạo Order với paymentType = "CASH"
        ↓
Mở dialog receipt (biên lai)
```

**Đặc điểm:**
- Không cần tích hợp bên ngoài
- Có gợi ý mệnh giá nhanh: 10k, 20k, 50k, 100k, 200k, 500k
- Validate: tiền khách đưa ≥ tổng tiền mới cho xác nhận

---

### 2.2 💳 Thẻ ngân hàng (CARD)

**Luồng:**
```
Cashier chọn "Thẻ ngân hàng"
        ↓
Khách quẹt thẻ qua máy POS vật lý (ngoài hệ thống)
        ↓
Cashier bấm "Đã quẹt thẻ thành công" (xác nhận thủ công)
        ↓
Backend tạo Order với paymentType = "CARD"
```

**Đặc điểm:**
- Hệ thống không tích hợp trực tiếp với máy POS thẻ
- Cashier là người xác nhận sau khi máy thẻ thành công
- Phù hợp với cửa hàng đã có máy POS thẻ riêng

---

### 2.3 📱 QR Chuyển khoản — SePay (UPI)

Đây là phương thức **tích hợp thực tế** với ngân hàng. Chi tiết ở mục 3.

---

## 3. Luồng thanh toán QR — Chi tiết kỹ thuật

### 3.1 Sơ đồ luồng đầy đủ

```
CASHIER chọn "Chuyển khoản QR"
         │
         ▼
[FE] Tạo mã đơn hàng ngẫu nhiên
     qrOrderRef = "DH" + 7 chữ số cuối timestamp
     VD: "DH4610579"
         │
         ▼
[FE → BE] POST /api/qr-payments/register
     Body: { orderRef: "DH4610579", amount: 372000 }
     → Backend lưu session vào ConcurrentHashMap
         │
         ▼
[FE] Hiển thị QR code từ SePay:
     https://qr.sepay.vn/img
       ?acc=VQRQAJOHG9152
       &bank=MBBank
       &amount=372000
       &des=DH4610579
         │
         ├──────────────────────────────────────────┐
         │                                          │
         ▼                                          ▼
[FE] Poll /api/qr-payments/status/DH4610579    [BE] @Scheduled mỗi 4 giây
     mỗi 3 giây                                 GET SePay API transactions/list
                                                 ?since_id=lastKnownId
         │                                          │
         │                                          ▼
KHÁCH quẹt QR → chuyển khoản                [BE] Tìm "DH4610579" trong
nội dung: "DH4610579"                             transaction_content
         │                                          │
         ▼                                          ▼
MB Bank ghi nhận giao dịch              [BE] confirmPayment("DH4610579", amount)
         │                                   → session.markPaid()
         ▼                                          │
SePay đọc giao dịch mới ────────────────────────────┘
         │
         ▼
[FE] Poll nhận được status = "PAID"
         │
         ▼
[FE] Tự động gọi processPayment(isAutoConfirm=true)
         │
         ▼
[FE → BE] POST /api/orders → Tạo đơn hàng trong DB
         │
         ▼
[FE] DELETE /api/qr-payments/DH4610579 (cleanup)
     Đóng dialog → Mở receipt 🎉
```

---

### 3.2 Giải thích từng bước

#### Bước 1: Tạo mã đơn hàng (Order Reference)

```javascript
// PaymentDialog.jsx
qrOrderRef.current = `DH${Date.now().toString().slice(-7)}`
// Kết quả: "DH4610579"
```

**Mục đích:** Mã này là "key" để khớp giao dịch ngân hàng với đơn hàng trong hệ thống.
Khách chuyển khoản phải ghi đúng mã này vào nội dung (QR đã nhúng sẵn).

#### Bước 2: Đăng ký session

```javascript
// Frontend gọi backend để "đăng ký" đang chờ thanh toán
await api.post("/api/qr-payments/register", {
  orderRef: "DH4610579",
  amount: 372000
});
```

```java
// QrPaymentSessionService.java — lưu in-memory
sessions.put("DH4610579", new QrSession("DH4610579", 372000));
```

#### Bước 3: Tạo QR Code

SePay cung cấp API tạo ảnh QR theo chuẩn VietQR:
```
https://qr.sepay.vn/img
  ?acc=VQRQAJOHG9152   ← Số tài khoản VA (Virtual Account)
  &bank=MBBank          ← Ngân hàng
  &amount=372000        ← Số tiền (VND, số nguyên)
  &des=DH4610579        ← Nội dung chuyển khoản
```

> **Virtual Account (VA):** SePay cấp cho mỗi tài khoản một số VA riêng.
> Tiền chuyển vào VA → tự động vào tài khoản chính (9999999998628).

#### Bước 4: Polling song song

**Frontend poll** (mỗi 3 giây):
```javascript
setInterval(async () => {
  const res = await api.get(`/api/qr-payments/status/${ref}`);
  if (res.data.status === "PAID") {
    stopPolling();
    await processPayment(true); // auto-confirm
  }
}, 3000);
```

**Backend poll SePay** (mỗi 4 giây):
```java
@Scheduled(fixedDelay = 4000)
public void pollTransactions() {
  // GET https://my.sepay.vn/userapi/transactions/list?since_id=lastId
  // Tìm "DH4610579" trong transaction_content
  // Nếu tìm thấy → session.markPaid()
}
```

#### Bước 5: Tự động xác nhận

Khi backend phát hiện giao dịch → đánh dấu session là PAID.
Frontend đang poll → nhận được PAID → tự gọi `processPayment(true)` → tạo đơn hàng.

---

### 3.3 Cấu trúc JSON SePay API

**Request:**
```http
GET https://my.sepay.vn/userapi/transactions/list?since_id=49682&limit=20
Authorization: Bearer {API_TOKEN}
```

**Response:**
```json
{
  "status": 200,
  "error": null,
  "messages": { "success": true },
  "transactions": [
    {
      "id": "49683",
      "transaction_date": "2024-01-01 10:30:00",
      "account_number": "VQRQAJOHG9152",
      "amount_in": "372000.00",
      "amount_out": "0.00",
      "transaction_content": "DH4610579 chuyen khoan thanh toan",
      "reference_number": "FT24001...",
      "bank_brand_name": "MB Bank"
    }
  ]
}
```

> **Lưu ý kỹ thuật:** `amount_in` là **String thập phân** (`"372000.00"`), không phải số nguyên.
> Phải dùng `Double.parseDouble()` rồi cast sang `long`.

---

## 4. Kiến trúc SePay Polling

### 4.1 Tại sao không dùng Webhook?

| | Webhook | API Polling (đã chọn) |
|---|---|---|
| Cần URL public | ✅ Có (cần deploy/ngrok) | ❌ Không |
| Phù hợp localhost | ❌ | ✅ |
| Độ trễ | ~1 giây | ~4 giây |
| Phù hợp đồ án | Khó demo | ✅ Dễ demo |

**Giải thích:**
Webhook yêu cầu SePay gọi ngược về server của bạn (`POST http://your-server/webhook`).
Khi chạy localhost, SePay không thể gọi vào `localhost:8080`.
API Polling: backend **chủ động hỏi** SePay — không cần public URL.

### 4.2 Cơ chế `since_id`

```
Lần 1 (khởi động backend):
  - Lấy 20 giao dịch gần nhất
  - Lưu ID giao dịch mới nhất: lastSeenId = "49682"
  - KHÔNG process (tránh confirm giao dịch cũ từ hôm qua)

Lần 2+ (mỗi 4 giây):
  - GET /transactions/list?since_id=49682
  - SePay chỉ trả về giao dịch có ID > 49682
  - Đây là giao dịch THỰC SỰ MỚI
  - Tìm mã DH → nếu có → confirm session
  - Cập nhật lastSeenId = ID mới nhất nhận được
```

**Tại sao dùng `since_id` tốt hơn `transaction_date_min`?**
- `since_id`: Chính xác tuyệt đối, không bị lỗi timezone
- `transaction_date_min`: Có thể bị lệch múi giờ server vs SePay

---

## 5. Cấu trúc code

### 5.1 Backend — Các file quan trọng

```
src/main/java/com/zosh/
├── controller/
│   ├── QrPaymentController.java       ← API cho FE (register/status/cleanup)
│   └── SepayWebhookController.java    ← Webhook + simulate endpoint
├── service/
│   ├── QrPaymentSessionService.java   ← Quản lý session in-memory
│   └── SepayPollingService.java       ← Tự động poll SePay mỗi 4s
└── PosSystemApplication.java          ← @EnableScheduling, RestTemplate bean
```

**QrPaymentController** — REST API:
```
POST   /api/qr-payments/register     FE đăng ký session mới
GET    /api/qr-payments/status/{ref} FE poll trạng thái
DELETE /api/qr-payments/{ref}        FE cleanup sau khi tạo order
```

**QrPaymentSessionService** — Business logic:
```java
registerSession(ref, amount)   // Lưu session vào ConcurrentHashMap
checkStatus(ref)               // → "PENDING" | "PAID" | "NOT_FOUND"
confirmPayment(ref, amount)    // Mark paid, check số tiền ±1000đ
hasPendingSessions()           // Kiểm tra có session nào đang chờ không
extractOrderRef(content)       // Regex tìm "DH[0-9]{5,10}" trong nội dung
```

### 5.2 Frontend — PaymentDialog.jsx

**State quan trọng:**
```javascript
const [qrPollingStatus, setQrPollingStatus] = useState("IDLE");
// IDLE → WAITING → PAID (hoặc ERROR)

const pollingIntervalRef = useRef(null);    // Ref tới setInterval
const qrOrderRef = useRef(`DH${...}`);     // Mã đơn hàng hiện tại
```

---

## 6. Cấu hình hệ thống

### 6.1 application.yml

```yaml
sepay:
  api:
    token: KEBEVIZFFTGZDYUHU7OHNX0TULS4QYJPKRQPWF5BKOICN5LUYGJRL6ICMAMOSCW1
  account:
    number: VQRQAJOHG9152
```

### 6.2 Tài khoản SePay

| Thông tin | Giá trị |
|-----------|---------|
| Ngân hàng | MBBank |
| Tài khoản VA | VQRQAJOHG9152 |
| Tài khoản chính | 9999999998628 |
| Chủ tài khoản | HOANG NHU VIET |

---

## 7. Câu hỏi phỏng vấn thường gặp

---

### ❓ "Hệ thống thanh toán của em hoạt động như thế nào?"

> Hệ thống POS của em có 3 phương thức thanh toán: tiền mặt, thẻ ngân hàng và QR chuyển khoản.
>
> Phương thức QR được tích hợp thực tế với cổng thanh toán **SePay** — trung gian kết nối với ngân hàng MBBank thông qua Virtual Account.
>
> Luồng hoạt động: cashier chọn QR → hệ thống tạo mã đơn ngẫu nhiên (VD: DH4610579) → hiển thị QR đã nhúng sẵn số tiền và mã. Khách quét QR chuyển khoản. Backend tự động poll SePay mỗi 4 giây, phát hiện giao dịch khớp mã → xác nhận và tạo đơn hàng tự động.

---

### ❓ "Tại sao em dùng polling thay vì webhook?"

> Webhook yêu cầu SePay gọi ngược về server của em — cần địa chỉ public. Trong môi trường localhost, điều này không khả thi mà không cần ngrok.
>
> API Polling: backend chủ động hỏi SePay mỗi 4 giây — không cần public URL, chạy được ngay trên localhost. Độ trễ tối đa 4 giây vẫn chấp nhận được cho môi trường POS.
>
> Nếu deploy lên server thật, chuyển sang webhook giảm độ trễ xuống ~1 giây.

---

### ❓ "Em xử lý trường hợp nhiều khách thanh toán QR đồng thời thế nào?"

> Em dùng **ConcurrentHashMap** — thread-safe trong Java. Mỗi session có key là mã đơn hàng độc nhất (DH + timestamp), nên nhiều giao dịch song song không xung đột. Với mỗi giao dịch từ SePay, backend tìm mã DH bằng regex và chỉ xác nhận đúng session tương ứng.

---

### ❓ "Làm sao em biết giao dịch đúng hay sai?"

> Em kiểm tra 2 điều kiện:
> 1. **Mã đơn hàng**: Nội dung chuyển khoản phải chứa mã DHxxxxxxx (regex `DH\d{5,10}`)
> 2. **Số tiền**: Số tiền phải khớp với tổng đơn, cho phép sai lệch ±1,000đ (do làm tròn)
>
> Nếu một trong hai không khớp, giao dịch bị bỏ qua, session vẫn PENDING.

---

### ❓ "Em lưu trạng thái session ở đâu? Tại sao không dùng database?"

> Em lưu in-memory bằng ConcurrentHashMap vì:
> - Session tồn tại ngắn (vài phút) — không cần persist
> - Truy cập O(1), phù hợp polling tần suất cao
> - Sau khi tạo đơn thành công, session xóa ngay
>
> Trade-off: nếu backend restart, session mất. Production nên dùng Redis để persist và share state giữa nhiều instance.

---

### ❓ "SePay là gì? Tại sao em chọn SePay?"

> SePay là cổng trung gian kết nối với hệ thống ngân hàng Việt Nam. Thay vì ký hợp đồng trực tiếp với ngân hàng (phức tạp, mất nhiều tháng), SePay cung cấp:
> - **Virtual Account (VA)**: Số tài khoản ảo nhận thanh toán, forward vào tài khoản chính
> - **Transaction API**: Query giao dịch — em dùng để polling
> - **QR Generator**: Tạo ảnh QR chuẩn VietQR, nhúng sẵn số tiền và nội dung
>
> Em chọn SePay vì miễn phí cho mức độ đồ án và có tài liệu rõ ràng.

---

### ❓ "Nếu mạng mất giữa chừng thì sao?"

> - **FE mất mạng**: Polling dừng, cashier thấy badge lỗi. Khi mạng phục hồi, có thể bấm xác nhận thủ công.
> - **BE mất kết nối SePay**: Poll lỗi được catch và log, không crash. Tự phục hồi khi mạng về.
> - **BE restart**: `lastSeenId` reset → re-init từ giao dịch mới nhất. Giao dịch xảy ra trong lúc restart cần cashier xác nhận thủ công. Đây là trade-off của in-memory solution.

---

## 📌 Tóm tắt để nhớ nhanh

```
QR Payment Flow (3 dòng):
1. FE tạo mã DH → đăng ký với BE → hiển thị QR SePay (có nhúng số tiền + mã)
2. Khách quét QR → chuyển khoản → SePay ghi nhận → BE poll mỗi 4s → phát hiện mã DH
3. BE mark PAID → FE poll nhận PAID → tự tạo order → đóng dialog → mở receipt
```

**3 file backend quan trọng nhất:**
- `QrPaymentSessionService` — não của luồng, quản lý trạng thái
- `SepayPollingService` — mắt của luồng, phát hiện giao dịch
- `QrPaymentController` — tai của luồng, nhận request từ FE

---

*Đồ án tốt nghiệp — POS System*
