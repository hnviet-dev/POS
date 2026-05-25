# KỸ THUẬT & NGHIỆP VỤ XỬ LÝ — ZOSH POS

> Tài liệu này giải thích **TẠI SAO** và **NHƯ THẾ NÀO** các kỹ thuật được áp dụng trong hệ thống — từ bảo mật, xử lý nghiệp vụ phức tạp đến tối ưu hiệu năng.

---

## 1. STATELESS JWT AUTHENTICATION

### 1.1 Vấn đề & Giải pháp

**Vấn đề:** HTTP là giao thức không trạng thái (stateless). Server không nhớ ai đã đăng nhập giữa các request.

**Giải pháp cũ (Session):** Server lưu session ID trong bộ nhớ → không scale được khi nhiều server.

**Giải pháp hiện tại (JWT):** Token mang thông tin ngay trong chính nó, server chỉ cần kiểm tra chữ ký, không cần lưu gì.

### 1.2 Cấu trúc JWT Token

```
eyJhbGciOiJIUzUxMiJ9          ← Header (thuật toán HS512)
.eyJlbWFpbCI6InVzZXJAZXguY29tIiwiYXV0aG9yaXRpZXMiOiJST0xFX1NUT1JFX0FETUlOIiwiaWF0IjoxNzAwMDAwLCJleHAiOjE3MDAwODY0MDB9
                                ← Payload (base64 của JSON bên dưới)
.SIGNATURE                      ← HMAC-SHA512(header.payload, SECRET_KEY)

// Payload sau khi decode:
{
  "email": "user@example.com",
  "authorities": "ROLE_STORE_ADMIN",
  "iat": 1700000000,    // issued at
  "exp": 1700086400     // expired at (24 giờ sau)
}
```

### 1.3 Luồng kỹ thuật (từng dòng code)

```
JwtProvider.generateToken(Authentication auth):
  → Claims claims = Jwts.claims()
  → claims.put("email", username)
  → claims.put("authorities", auth.getAuthorities().toString())
  → Jwts.builder()
         .setClaims(claims)
         .signWith(key, SignatureAlgorithm.HS512)
         .setExpiration(new Date(now + 86400000))  // 24h
         .compact()                                  // → JWT string

JwtValidator.doFilterInternal() [chạy mỗi request]:
  → String jwt = header.substring(7)                // Bỏ "Bearer "
  → Claims claims = Jwts.parser()
                        .verifyWith(key)
                        .parseSignedClaims(jwt)
                        .getPayload()
  → String email = claims.get("email")
  → String authorities = claims.get("authorities")
  → Authentication auth = new UsernamePasswordAuthenticationToken(
         email,
         null,
         List.of(new SimpleGrantedAuthority(authorities))
    )
  → SecurityContextHolder.getContext().setAuthentication(auth)
```

### 1.4 Điểm mạnh của thiết kế này

| Tính chất | Lý do |
|---|---|
| **Stateless** | Server không lưu session, dễ scale ngang (horizontal scaling) |
| **Self-contained** | Token chứa đủ thông tin role, service không cần query DB để biết quyền |
| **Tamper-proof** | Chữ ký HMAC-SHA512 — nếu client sửa payload, server phát hiện ngay |
| **24h expiry** | Giảm rủi ro token bị đánh cắp (short-lived) |

---

## 2. RBAC + DATA ISOLATION (Multi-Tenant Pattern)

### 2.1 Hai lớp bảo vệ

Hệ thống dùng **2 lớp** kiểm soát truy cập, không chỉ dùng 1:

```
Lớp 1 — Role-based (Ai được gọi API này?):
  @PreAuthorize("hasRole('BRANCH_CASHIER')")  // Chỉ cashier
  @PreAuthorize("hasAnyRole('STORE_ADMIN','STORE_MANAGER')")

Lớp 2 — Data-based (Có được xem DATA này không?):
  User currentUser = getCurrentUser()         // Từ SecurityContext
  if (!product.getStore().equals(currentUser.getStore()))
      throw new AccessDeniedException(...)    // Đúng role nhưng sai store
```

### 2.2 checkAuthority() pattern

```java
// ProductServiceImpl.java
private void checkAuthority(Store store, User currentUser) {
    boolean isStoreManager = currentUser.getRole() == ROLE_STORE_MANAGER
                          && currentUser.getStore().equals(store);
    boolean isStoreAdmin   = currentUser.getRole() == ROLE_STORE_ADMIN
                          && store.getStoreAdmin().equals(currentUser);

    if (!isStoreManager && !isStoreAdmin) {
        throw new AccessDeniedException("Không có quyền quản lý store này");
    }
}
// Hàm này được gọi trước EVERY thao tác create/update/delete sản phẩm
```

### 2.3 Data Isolation trong Query

```java
// OrderServiceImpl — Lấy đơn hàng theo chi nhánh
// Không bao giờ SELECT * FROM orders
// Luôn filter theo branchId của user hiện tại

List<Order> orders = orderRepository.findByBranchId(branch.getId());
// → SQL: WHERE branch_id = ? (branch của cashier đang đăng nhập)

// BranchAnalyticsServiceImpl — Doanh thu theo ngày
BigDecimal total = orderRepository.getTotalSalesBetween(
    branchId,   // ← Luôn gắn với branch cụ thể
    startTime,
    endTime
);
```

**Kết quả:** Chi nhánh A không bao giờ thấy dữ liệu của Chi nhánh B, Store A không thấy dữ liệu Store B — dù họ dùng chung 1 database.

---

## 3. CART STATE MACHINE (Local State Pattern)

### 3.1 Tại sao không gọi API khi tính tiền?

Môi trường POS yêu cầu **zero latency**. Mỗi lần cashier thêm món, điều chỉnh số lượng, áp mã giảm giá — nếu phải đợi API response (50-200ms mỗi lần) sẽ làm chậm toàn bộ quy trình bán hàng.

**Giải pháp:** `cartSlice` là một **State Machine thuần Frontend**, tính toán mọi con số ngay tại trình duyệt:

```
Trạng thái giỏ hàng:
  EMPTY ──addItem──→ HAS_ITEMS
  HAS_ITEMS ──setDiscount──→ HAS_ITEMS (recalculate)
  HAS_ITEMS ──holdOrder──→ EMPTY (items → holdOrders[])
  HAS_ITEMS ──checkout──→ EMPTY (sau khi API thành công)
  holdOrders[] ──restoreOrder──→ HAS_ITEMS
```

### 3.2 Công thức tính tiền

```
subtotal      = Σ(item.sellingPrice × item.quantity)
discountAmt   = subtotal × (discount / 100)
afterDiscount = subtotal − discountAmt
taxAmount     = afterDiscount × (taxRate / 100)
total         = afterDiscount + taxAmount
```

### 3.3 Backend Re-validation (Anti-fraud)

Khi FE gọi `POST /api/orders`, backend **KHÔNG tin** giá từ FE:

```java
// OrderServiceImpl.java
for (OrderItemRequest itemReq : dto.getItems()) {
    Product product = productRepo.findById(itemReq.getProductId())
                                 .orElseThrow();
    // Lấy giá THỰC TẾ từ DB, không dùng giá FE gửi lên
    double price = product.getSellingPrice() * itemReq.getQuantity();
    orderItem.setPrice(price);
}
// → Ngăn chặn hacker sửa giá trong request body
```

---

## 4. SHIFT REPORT AGGREGATION ALGORITHM

### 4.1 Bài toán nghiệp vụ

Khi ca làm việc kết thúc, hệ thống phải:
- Tổng hợp toàn bộ giao dịch trong ca (có thể hàng trăm đơn)
- Phân tích theo nhiều chiều (phương thức TT, sản phẩm, thời gian)
- Thực hiện nhanh để cashier không phải đợi lâu

### 4.2 Thuật toán xử lý

```java
// ShiftReportServiceImpl.closeShift()

// Bước 1: Xác định khoảng thời gian ca
ShiftReport shift = repo.findTopByCashierAndShiftEndIsNull(cashier);
LocalDateTime from = shift.getShiftStart();
LocalDateTime to   = LocalDateTime.now();
shift.setShiftEnd(to);

// Bước 2: Query toàn bộ dữ liệu
List<Order>  orders  = orderRepo.findByCashierAndBranchAndCreatedAtBetween(...);
List<Refund> refunds = refundRepo.findByCashierAndCreatedAtBetween(...);

// Bước 3: Tính tổng (Java Stream)
double totalSales   = orders.stream()
    .mapToDouble(o -> o.getTotalAmount().doubleValue()).sum();

double totalRefunds = refunds.stream()
    .mapToDouble(Refund::getAmount).sum();

double netSales = totalSales - totalRefunds;

// Bước 4: Phân tích Payment Breakdown
Map<PaymentType, DoubleSummaryStatistics> breakdown = orders.stream()
    .collect(Collectors.groupingBy(
        Order::getPaymentType,
        Collectors.summarizingDouble(o -> o.getTotalAmount().doubleValue())
    ));
// → { CASH: {sum:1500000, count:12}, CARD: {sum:800000, count:5}, ... }

// Bước 5: Top 5 sản phẩm bán chạy
// (join qua OrderItems, group by productId, sort by quantity DESC, limit 5)
List<Product> topProducts = orderItemRepo
    .getTopProductsByQuantity(branchId)
    .stream().limit(5)...

// Bước 6: Lưu tất cả vào DB một lần
shift.setTotalSales(totalSales);
shift.setTotalRefunds(totalRefunds);
shift.setNetSales(netSales);
shiftRepo.save(shift);
```

### 4.3 Vì sao tính tại Backend, không tính tại Frontend?

- **Tính toàn vẹn:** Con số doanh thu phải chính xác 100%, không thể để FE tính rồi gửi lên
- **Bảo mật:** Cashier không thể "tự báo cáo" doanh thu của mình
- **Lịch sử:** Kết quả được lưu vĩnh viễn vào DB để đối soát sau

---

## 5. EVENT-DRIVEN PAYMENT ARCHITECTURE

### 5.1 Vấn đề: Tight Coupling

Nếu sau khi thanh toán thành công ta gọi thẳng:
```java
subscriptionService.activate(subscriptionId);  // Kích hoạt sub
emailService.sendConfirmation(user);            // Gửi email
inventoryService.update(...);                   // Cập nhật kho (nếu cần)
```
→ PaymentService biết quá nhiều thứ → khó test, khó mở rộng.

### 5.2 Giải pháp: Spring Application Events

```java
// PaymentServiceImpl.java — Sau khi verify thành công:
PaymentSuccessEvent event = PaymentSuccessEvent.builder()
    .paymentId(payment.getId())
    .subscriptionId(...)
    .amount(...)
    .build();
paymentEventPublisher.publishPaymentSuccess(event);
// → PaymentService KHÔNG biết ai sẽ xử lý event này

// Ở đâu đó khác (SubscriptionEventListener.java):
@EventListener
public void handlePaymentSuccess(PaymentSuccessEvent event) {
    subscriptionService.activate(event.getSubscriptionId());
    emailService.sendWelcome(event.getStoreId());
}
```

### 5.3 Lợi ích

| Vấn đề cũ | Sau khi dùng Events |
|---|---|
| PaymentService phụ thuộc vào 5 services khác | Chỉ phụ thuộc vào EventPublisher |
| Thêm tính năng mới (VD: push notification) phải sửa PaymentService | Chỉ cần thêm `@EventListener` mới |
| Khó unit test | Test riêng từng listener |

---

## 6. ANALYTICS — KỸ THUẬT QUERY PHỨC TẠP

### 6.1 Daily Sales Chart (vòng lặp N ngày)

```java
// BranchAnalyticsServiceImpl.getDailySalesChart(branchId, days=7)
for (int i = 0; i < days; i++) {
    LocalDate date = today.minusDays(days - 1 - i);
    LocalDateTime start = date.atStartOfDay();
    LocalDateTime end   = date.atTime(LocalTime.MAX);

    // Mỗi ngày: 1 query database
    BigDecimal total = orderRepo
        .getTotalSalesBetween(branchId, start, end)
        .orElse(BigDecimal.ZERO);

    result.add(new DailySalesDTO(date, total));
}
// → 7 queries DB, mỗi query cho 1 ngày
// PHẦN NÀY CÓ THỂ CẢI THIỆN: dùng 1 query GROUP BY DATE thay vì vòng lặp
```

### 6.2 Top Products (Native JPQL Query)

```java
// OrderItemRepository.java
@Query("""
    SELECT oi.product.id, oi.product.name, SUM(oi.quantity) as totalQty
    FROM OrderItem oi
    WHERE oi.order.branch.id = :branchId
    GROUP BY oi.product.id, oi.product.name
    ORDER BY totalQty DESC
""")
List<Object[]> getTopProductsByQuantity(@Param("branchId") Long branchId);
```

### 6.3 Growth % Calculation (Today vs Yesterday)

```java
// BranchAnalyticsServiceImpl.getBranchOverview()
private double calculateGrowth(Number today, Number yesterday) {
    if (yesterday == null || yesterday.doubleValue() == 0.0)
        return 0.0;  // Tránh chia cho 0
    return ((today.doubleValue() - yesterday.doubleValue())
            / yesterday.doubleValue()) * 100;
}
// VD: Hôm nay: 5tr, hôm qua: 4tr → growth = (5-4)/4 × 100 = +25%
//     Hôm nay: 3tr, hôm qua: 4tr → growth = (3-4)/4 × 100 = -25%
```

### 6.4 Monthly Sales Grouping (Java Stream)

```java
// StoreAnalyticsServiceImpl.getMonthlySalesGraph()
List<Order> orders = orderRepo.findAllByStoreAdminAndCreatedAtBetween(
    storeAdminId, now.minusDays(365), now
);

Map<YearMonth, Double> grouped = orders.stream()
    .collect(Collectors.groupingBy(
        order -> YearMonth.from(order.getCreatedAt()),    // Group by month
        Collectors.summingDouble(order ->
            order.getTotalAmount().doubleValue()           // Sum revenue
        )
    ));

return grouped.entrySet().stream()
    .sorted(Map.Entry.comparingByKey())                   // Sort chronologically
    .map(e -> new TimeSeriesPointDTO(
        e.getKey().atDay(1).atStartOfDay(),               // YearMonth → DateTime
        e.getValue()
    ))
    .collect(Collectors.toList());
```

---

## 7. CLOUDINARY DIRECT UPLOAD PATTERN

### 7.1 Vấn đề với Upload thông thường

Thông thường: `FE → BE → Cloudinary` (ảnh phải qua server → tốn bandwidth, chậm).

### 7.2 Giải pháp: Direct Upload từ Browser

```
FE → Cloudinary (TRỰC TIẾP)     // Không qua backend
FE nhận URL ảnh
FE gửi URL (text) → BE          // Backend chỉ lưu URL string
```

```javascript
// uploadToCloudinary.js
export const uploadToCloudinary = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", CLOUDINARY_PRESET);  // Preset public

    const res = await axios.post(
        `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/image/upload`,
        formData
    );
    return res.data.secure_url;  // → "https://res.cloudinary.com/..."
};

// ProductForm.jsx
const imageUrl = await uploadToCloudinary(file);
dispatch(createProduct({ ...productData, image: imageUrl }));
```

**Lợi ích:** Backend không cần xử lý file, không tốn RAM/storage server.

---

## 8. PASSWORD RESET — SECURE TOKEN FLOW

### 8.1 Cơ chế kỹ thuật

```java
// AuthServiceImpl.forgotPassword(email)
String token = UUID.randomUUID().toString();  // Random, không đoán được
LocalDateTime expiry = LocalDateTime.now().plusMinutes(5);  // Hết hạn sau 5 phút

PasswordResetToken resetToken = PasswordResetToken.builder()
    .token(token)
    .user(user)
    .expiryDate(expiry)
    .build();
tokenRepo.save(resetToken);

// Gửi email chứa link:
String link = frontendUrl + "/reset-password?token=" + token;
emailService.sendResetEmail(user.getEmail(), link);
```

```java
// AuthServiceImpl.resetPassword(token, newPassword)
PasswordResetToken resetToken = tokenRepo.findByToken(token);
if (resetToken.isExpired()) {      // isExpired() = expiryDate.isBefore(now())
    tokenRepo.delete(resetToken);
    throw new RuntimeException("Token đã hết hạn");
}
user.setPassword(passwordEncoder.encode(newPassword));
userRepo.save(user);
tokenRepo.delete(resetToken);      // Dùng 1 lần rồi xóa (one-time use)
```

### 8.2 Điểm bảo mật quan trọng

| Cơ chế | Giải thích |
|---|---|
| Token là UUID random | Không thể đoán/brute-force |
| Hết hạn 5 phút | Giảm cửa sổ tấn công nếu email bị lộ |
| One-time use | Sau khi dùng xong, token bị xóa ngay |
| Unique constraint trên token | Không có 2 token giống nhau trong DB |

---

## 9. DESIGN PATTERNS ÁP DỤNG

| Pattern | Áp dụng ở đâu | Lý do |
|---|---|---|
| **Repository Pattern** | Tất cả JPA Repositories | Tách biệt logic business với data access |
| **DTO Pattern** | 30+ DTO classes, 12 Mappers | Không expose Entity ra ngoài (bảo mật password, tránh circular JSON) |
| **Builder Pattern** | Mọi Entity, DTO, Event class | Code tạo object rõ ràng, không nhầm lẫn thứ tự tham số |
| **Observer/Event Pattern** | Payment Events | Decoupling giữa Payment và Subscription/Email |
| **Strategy Pattern** | RazorpayService, StripeService | Dễ thêm cổng thanh toán mới mà không sửa code cũ |
| **State Machine** | cartSlice, ShiftReport | Quản lý trạng thái phức tạp có thể đoán được |
| **Factory (Implicit)** | DataInitializationComponent | Tự tạo Super Admin khi khởi động |
| **Filter Chain** | JwtValidator | Xử lý xác thực trước khi request đến Controller |

---

## 10. ĐIỂM CẦN CẢI THIỆN (Ghi chú kỹ thuật)

| Vấn đề | Vị trí | Đề xuất |
|---|---|---|
| N+1 query trong daily sales chart | `BranchAnalyticsServiceImpl` | Thay vòng lặp 7 query bằng 1 query `GROUP BY DATE` |
| `yesterdayLowStock: 12` hardcode | `BranchAnalyticsServiceImpl:159` | Lưu snapshot vào Redis hoặc bảng riêng |
| JWT secret key hardcode | `JwtConstant.java` | Chuyển vào `application.yml` hoặc env variable |
| `expirePastSubscriptions()` chưa có Scheduler | `SubscriptionServiceImpl` | Thêm `@Scheduled(cron="0 0 * * *")` để tự động chạy hàng ngày |
| Stripe chỉ là stub (trả về mock data) | `StripeService.java` | Tích hợp Stripe SDK thực tế nếu cần |
