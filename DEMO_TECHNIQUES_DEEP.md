# KỸ THUẬT SÂU — FRONTEND & BACKEND — DEMO ĐỒ ÁN

---

## FRONTEND — KỸ THUẬT NỔI BẬT

### FE-1: Redux Toolkit — Optimistic State Management

**Vấn đề thực tế:** Khi thu ngân thêm sản phẩm vào giỏ, nếu phải đợi API trả về mới cập nhật UI → lag, trải nghiệm tệ.

**Kỹ thuật:** `cartSlice` dùng **local state** — mọi thao tác giỏ hàng xảy ra *synchronously* trong Redux, không có API nào được gọi:

```javascript
// cartSlice.js — addItem reducer
addItem: (state, action) => {
  const product = action.payload;
  const existing = state.items.find(i => i.id === product.id);
  if (existing) {
    existing.quantity += 1;
  } else {
    state.items.push({ ...product, quantity: 1 });
  }
  recalculate(state);  // Tính lại total ngay lập tức
}

// recalculate chạy sau MỌI reducer
const recalculate = (state) => {
  state.subtotal = state.items.reduce(
    (sum, i) => sum + i.sellingPrice * i.quantity, 0
  );
  state.discountAmount = state.subtotal * (state.discount / 100);
  state.taxAmount = (state.subtotal - state.discountAmount) * (state.taxRate / 100);
  state.total = state.subtotal - state.discountAmount + state.taxAmount;
};
```

**Demo point:** Thêm 10 sản phẩm liên tiếp cực nhanh, số tổng tiền nhảy ngay lập tức — không lag 1 giây.

---

### FE-2: Role-Based Routing Guard

**Kỹ thuật:** `App.jsx` đóng vai trò **Route Guard** — đọc `user.role` từ Redux store, render *đúng bộ route* cho từng vai trò:

```jsx
// App.jsx — logic điều hướng
const { user } = useSelector(state => state.auth);

const getRoutes = () => {
  switch(user?.role) {
    case 'ROLE_ADMIN':           return <SuperAdminRoutes />;
    case 'ROLE_STORE_ADMIN':
    case 'ROLE_STORE_MANAGER':   return <StoreAdminRoutes />;
    case 'ROLE_BRANCH_MANAGER':
    case 'ROLE_BRANCH_ADMIN':    return <BranchManagerRoutes />;
    case 'ROLE_BRANCH_CASHIER':  return <CashierRoutes />;
    default:                     return <AuthRoutes />;
  }
};
```

**Demo point:** Đăng nhập bằng 3 tài khoản khác nhau — màn hình Dashboard hoàn toàn khác nhau, URL khác nhau. Nếu gõ tay URL `/super-admin/...` bằng tài khoản cashier → redirect về login.

---

### FE-3: Hold Order — Giỏ hàng Song song

**Vấn đề nghiệp vụ thực tế:** Khách A đang gọi món, bỗng khách B vào thanh toán nhanh → cashier cần "đỗ" đơn của khách A lại.

**Kỹ thuật:** `holdOrders` là *stack* (mảng các giỏ hàng), mỗi phần tử là 1 snapshot của cart state:

```javascript
// cartSlice.js
holdOrder: (state) => {
  if (state.items.length > 0) {
    state.holdOrders.push({          // Push snapshot vào stack
      items: [...state.items],
      customer: state.customer,
      discount: state.discount,
    });
    // Clear cart để tiếp khách mới
    state.items = [];
    state.customer = null;
    state.discount = 0;
    recalculate(state);
  }
},
restoreOrder: (state, action) => {
  const index = action.payload;
  const held = state.holdOrders[index];
  state.items    = held.items;       // Khôi phục giỏ cũ
  state.customer = held.customer;
  state.discount = held.discount;
  state.holdOrders.splice(index, 1); // Xóa khỏi stack
  recalculate(state);
},
```

**Demo point:** Mở 2 đơn song song trên cùng 1 màn hình cashier, chuyển đổi qua lại mượt mà.

---

### FE-4: Axios Interceptor — Tự động gắn JWT

**Kỹ thuật:** Thay vì mỗi thunk phải tự thêm header, `api.js` cấu hình **request interceptor** tự động inject token:

```javascript
// utils/api.js
const api = axios.create({ baseURL: 'http://localhost:5000' });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('jwt');  // Token hết hạn → logout
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);
```

**Demo point:** Mở DevTools → Network tab → Thấy tất cả request đều có `Authorization: Bearer eyJ...` tự động.

---

### FE-5: Cloudinary Direct Upload

**Kỹ thuật:** Ảnh được upload thẳng từ browser lên Cloudinary — server không cần xử lý file binary:

```javascript
// uploadToCloudinary.js
export const uploadImageToCloudinary = async (file) => {
  const data = new FormData();
  data.append("file", file);
  data.append("upload_preset", "your_preset"); // Unsigned preset

  const res = await axios.post(
    `https://api.cloudinary.com/v1_1/CLOUD_NAME/image/upload`, data
  );
  return res.data.secure_url; // URL ảnh trả về
};

// ProductForm.jsx dùng như sau:
const handleImageChange = async (e) => {
  const file = e.target.files[0];
  const url = await uploadImageToCloudinary(file);  // Upload lên cloud
  setProductData(prev => ({ ...prev, image: url })); // Lưu URL vào form
};
// → Chỉ gửi STRING URL xuống backend, không gửi file
```

**Demo point:** Chọn ảnh → thấy preview ngay lập tức, network call lên cloudinary.com (không phải localhost:5000).

---

## BACKEND — KỸ THUẬT NỔI BẬT

### BE-1: JWT Filter Chain — Zero Trust Architecture

**Kỹ thuật:** `JwtValidator` kế thừa `OncePerRequestFilter` → Spring Security đảm bảo nó chạy *chính xác 1 lần* mỗi request, trước khi đến Controller:

```java
// JwtValidator.java
@Override
protected void doFilterInternal(HttpServletRequest req,
                                 HttpServletResponse res,
                                 FilterChain chain) throws IOException, ServletException {
    String header = req.getHeader("Authorization");

    if (header != null && header.startsWith("Bearer ")) {
        String jwt = header.substring(7);
        try {
            Claims claims = Jwts.parser()
                .verifyWith(Keys.hmacShaKeyFor(SECRET_KEY.getBytes()))
                .build()
                .parseSignedClaims(jwt)
                .getPayload();

            String email       = claims.get("email", String.class);
            String authorities = claims.get("authorities", String.class);

            Authentication auth = new UsernamePasswordAuthenticationToken(
                email, null,
                List.of(new SimpleGrantedAuthority(authorities))
            );
            SecurityContextHolder.getContext().setAuthentication(auth);

        } catch (JwtException e) {
            // Token invalid/expired → SecurityContext trống
            // → Spring Security tự từ chối request (401)
        }
    }
    chain.doFilter(req, res); // Tiếp tục pipeline
}
```

**Demo point:** Gọi API `/api/orders` không có token → 401. Gọi với token của Cashier vào endpoint `/api/super-admin/...` → 403. Mở Postman live để show.

---

### BE-2: @PreAuthorize + Method Security

**Kỹ thuật:** Kiểm tra quyền tại tầng Controller bằng annotation, trước khi Service chạy:

```java
// OrderController.java
@PostMapping
@PreAuthorize("hasAuthority('ROLE_BRANCH_CASHIER')")
public ResponseEntity<Order> createOrder(@RequestBody OrderRequest dto,
                                          HttpServletRequest req) { ... }

@GetMapping("/recent/{branchId}")
@PreAuthorize("hasAnyAuthority('ROLE_BRANCH_MANAGER','ROLE_BRANCH_ADMIN')")
public ResponseEntity<List<Order>> getRecentOrders(@PathVariable Long branchId) { ... }

// StoreController.java
@PutMapping("/{storeId}/moderate")
@PreAuthorize("hasAuthority('ROLE_ADMIN')")  // Chỉ Super Admin
public ResponseEntity<?> moderateStore(...) { ... }
```

**Demo point:** Đăng nhập cashier → thử gọi API moderation store → 403 Forbidden. Giải thích: annotation này được Spring AOP wrap quanh method, gọi trước khi method body thực thi.

---

### BE-3: getCurrentUser() — Lấy Context từ SecurityContext

**Kỹ thuật:** Service layer không nhận `userId` từ request body (dễ giả mạo) mà đọc từ SecurityContext (đã được JwtValidator set):

```java
// UserServiceImpl.java
@Override
public User getCurrentUser() throws UserException {
    // Lấy Authentication đã được JwtValidator inject
    Authentication auth = SecurityContextHolder.getContext().getAuthentication();
    String email = auth.getName(); // Principal = email từ JWT

    User user = userRepo.findByEmail(email);
    if (user == null) throw new UserException("User not found");
    return user;
}

// Cách dùng trong mọi Service:
// OrderServiceImpl.createOrder()
User cashier = userService.getCurrentUser(); // Không cần request param
Branch branch = cashier.getBranch();         // Lấy branch từ user profile
```

**Demo point:** Hỏi: "Làm sao hệ thống biết order này của cashier nào?" → Trả lời: Không cần gửi `cashierId` trong request, hệ thống đọc từ JWT token → không thể giả mạo.

---

### BE-4: Data-Layer Isolation (Multi-Tenant Security)

**Kỹ thuật:** Mọi query luôn có điều kiện `storeId` hoặc `branchId` — không bao giờ trả toàn bộ data:

```java
// OrderRepository.java — Các query đều có scope
List<Order> findByBranchId(Long branchId);
List<Order> findByCashierAndBranchAndCreatedAtBetween(
    User cashier, Branch branch,
    LocalDateTime from, LocalDateTime to
);

// ProductRepository.java
@Query("SELECT p FROM Product p WHERE p.store.storeAdmin.id = :adminId")
List<Product> findByStoreAdminId(@Param("adminId") Long adminId);

// ProductServiceImpl.checkAuthority()
private void checkAuthority(Store store, User currentUser) {
    boolean ok = (currentUser.getRole() == STORE_MANAGER
                   && currentUser.getStore().equals(store))
               || (currentUser.getRole() == STORE_ADMIN
                   && store.getStoreAdmin().equals(currentUser));
    if (!ok) throw new AccessDeniedException("Không có quyền");
}
```

**Demo point:** Tạo 2 store, đăng nhập vào store A → Danh sách sản phẩm chỉ hiện của store A. Gọi API với storeId của store B → 403.

---

### BE-5: Shift Report — Aggregation Pipeline

**Kỹ thuật:** Khi đóng ca, hệ thống chạy pipeline tổng hợp dữ liệu:

```java
// ShiftReportServiceImpl.closeShift() — Pipeline 6 bước:

// B1: Đóng ca
ShiftReport shift = repo.findTopByCashierAndShiftEndIsNullOrderByShiftStartDesc(cashier)
    .orElseThrow(() -> new RuntimeException("No active shift"));
shift.setShiftEnd(LocalDateTime.now());

// B2: Query dữ liệu trong khoảng thời gian ca
List<Order> orders = orderRepo.findByCashierAndBranchAndCreatedAtBetween(
    cashier, branch, shift.getShiftStart(), shift.getShiftEnd());
List<Refund> refunds = refundRepo.findByCashierAndCreatedAtBetween(
    cashier, shift.getShiftStart(), shift.getShiftEnd());

// B3: Tính tổng bằng Stream
double totalSales   = orders.stream()
    .mapToDouble(o -> o.getTotalAmount().doubleValue()).sum();
double totalRefunds = refunds.stream()
    .mapToDouble(Refund::getAmount).sum();
double netSales     = totalSales - totalRefunds;

// B4: Payment Breakdown — group by PaymentType
Map<PaymentType, Double> byPayment = orders.stream()
    .collect(Collectors.groupingBy(
        Order::getPaymentType,
        Collectors.summingDouble(o -> o.getTotalAmount().doubleValue())
    ));
// → { CASH: 2500000.0, CARD: 800000.0, UPI: 300000.0 }

// B5: Top products — query native SQL
List<Object[]> topRaw = orderItemRepo.getTopProductsByQuantity(branch.getId());
List<Product> topProducts = topRaw.stream().limit(5)
    .map(row -> productRepo.findById((Long)row[0]).orElse(null))
    .collect(Collectors.toList());

// B6: Lưu và trả về
shift.setTotalSales(totalSales);
shift.setNetSales(netSales);
shift.setTotalOrders(orders.size());
shiftRepo.save(shift);
```

**Demo point:** Tạo 5-10 đơn hàng → End Shift → Báo cáo hiện đầy đủ: tổng tiền, số đơn, top sản phẩm, breakdown tiền mặt/thẻ. Mở DB trực tiếp show bảng `shift_report` đã được lưu.

---

### BE-6: Global Exception Handler — Unified Error Response

**Kỹ thuật:** `@ControllerAdvice` bắt toàn bộ exception từ mọi Controller, trả về format chuẩn:

```java
// GlobalExceptionHandler.java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserException.class)
    public ResponseEntity<ExceptionResponse> handleUser(UserException ex, WebRequest req) {
        return ResponseEntity.status(400).body(
            new ExceptionResponse(ex.getMessage(), req.getDescription(false), LocalDateTime.now())
        );
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<String> handleAccess(AccessDeniedException ex) {
        return ResponseEntity.status(403).body(ex.getMessage());
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ExceptionResponse> handleNotFound(ResourceNotFoundException ex, ...) {
        return ResponseEntity.status(404).body(...);
    }

    @ExceptionHandler(Exception.class) // Catch-all
    public ResponseEntity<ExceptionResponse> handleGeneral(Exception ex, ...) {
        return ResponseEntity.status(400).body(...);
    }
}
// Response format nhất quán:
// { "message": "...", "error": "uri=/api/...", "timestamp": "2024-..." }
```

**Demo point:** Gọi API sai (VD: productId không tồn tại) → Response JSON đẹp, có timestamp, có message rõ ràng thay vì stack trace lộn xộn.

---

### BE-7: Event-Driven Architecture cho Payment

**Kỹ thuật:** Sau khi verify thanh toán thành công, thay vì gọi thẳng nhiều service, `PaymentServiceImpl` publish 1 event:

```java
// PaymentServiceImpl.java
if (isValid) {
    payment.setStatus(PaymentStatus.SUCCESS);
    paymentRepo.save(payment);

    // Publish event — không biết ai sẽ xử lý
    PaymentSuccessEvent event = PaymentSuccessEvent.builder()
        .paymentId(payment.getId())
        .subscriptionId(payment.getSubscription().getId())
        .storeId(payment.getStore().getId())
        .paidAt(LocalDateTime.now())
        .build();
    paymentEventPublisher.publishPaymentSuccess(event);
}

// PaymentEventPublisher.java
@Component
public class PaymentEventPublisher {
    @Autowired ApplicationEventPublisher publisher;

    public void publishPaymentSuccess(PaymentSuccessEvent event) {
        publisher.publishEvent(event); // Spring sẽ tìm @EventListener
    }
}

// Các listener độc lập:
// SubscriptionEventListener.java
@EventListener
public void onPaymentSuccess(PaymentSuccessEvent event) {
    subscriptionService.activateSubscription(event.getSubscriptionId());
}
```

**Demo point:** Giải thích: "Nếu sau này cần gửi thêm push notification khi thanh toán thành công, chỉ cần thêm 1 `@EventListener` mới, không động vào `PaymentServiceImpl`."

---

## NHỮNG CÂU NÓI "GHI ĐIỂM" KHI DEMO

**Về Cart (FE):**
> "Em thiết kế giỏ hàng như một state machine thuần Frontend, zero API call, để đảm bảo thu ngân không bị lag. Backend chỉ được gọi khi checkout, và lúc đó backend sẽ re-validate lại toàn bộ giá từ database — phòng trường hợp có ai can thiệp vào request."

**Về Security (BE):**
> "Hệ thống có 2 lớp kiểm soát: lớp 1 là Role-based (ROLE_CASHIER mới được tạo order) qua `@PreAuthorize`. Lớp 2 là Data-based — cashier chỉ thấy order của chi nhánh mình, không thể xem của chi nhánh khác, dù đúng role, vì query luôn filter theo `branchId` của currentUser."

**Về Shift (BE):**
> "Đây là nghiệp vụ phức tạp nhất — khi cashier đóng ca, hệ thống không tính theo số liệu FE gửi lên, mà tự query lại toàn bộ orders và refunds trong khoảng thời gian ca từ database, rồi tính toán bằng Java Stream. Kết quả được lưu vĩnh viễn để đối soát sau."

**Về Multi-tenant (chung):**
> "Mỗi Store Admin chỉ thấy dữ liệu của store mình, dù hệ thống có hàng chục store khác dùng cùng database. Sự phân tách này được đảm bảo ở cả tầng API (JWT → getCurrentUser) lẫn tầng SQL query (WHERE store_id = ?)."
