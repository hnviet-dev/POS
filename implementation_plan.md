# Kế hoạch sửa: Enforce StoreStatus ACTIVE / PENDING / BLOCKED

## Bối cảnh vấn đề

Hiện tại `StoreStatus` (ACTIVE, PENDING, BLOCKED) chỉ có giá trị hiển thị trong Super Admin Dashboard, **không được enforce thực tế**. Store có status `PENDING` hoặc `BLOCKED` vẫn truy cập được mọi chức năng như `ACTIVE`.

## Phạm vi sửa

### 2 lớp cần sửa:
1. **Backend** – chặn API khi store không phải `ACTIVE`
2. **Frontend** – hiển thị trang thông báo đúng với từng trạng thái

---

## Phần 1: Backend (Spring Boot)

### [MODIFY] [StoreServiceImpl.java](file:///Users/Study/DOAN/z%20pos-source-code_1/pos-backend/src/main/java/com/zosh/service/impl/StoreServiceImpl.java)

Sửa `getStoreByAdminId()` – hiện đang trả về store bất kể status:

```java
// TRƯỚC (dòng 77-82) — không check status
public Store getStoreByAdminId() throws UserException {
    User currentUser = userService.getCurrentUser();
    return storeRepository.findByStoreAdminId(currentUser.getId());
}

// SAU — ném exception nếu PENDING hoặc BLOCKED
public Store getStoreByAdminId() throws UserException {
    User currentUser = userService.getCurrentUser();
    Store store = storeRepository.findByStoreAdminId(currentUser.getId());

    if (store == null) return null;

    if (store.getStatus() == StoreStatus.PENDING) {
        throw new UserException("STORE_PENDING: Your store is awaiting admin approval.");
    }
    if (store.getStatus() == StoreStatus.BLOCKED) {
        throw new UserException("STORE_BLOCKED: Your store has been blocked by the administrator.");
    }
    return store; // ACTIVE
}
```

> **Lý do dùng prefix message code** (`STORE_PENDING:`, `STORE_BLOCKED:`): frontend đọc message để biết redirect về trang nào.

---

## Phần 2: Frontend (React)

### [NEW] `src/pages/common/StorePending.jsx`

Trang hiển thị khi store đang chờ duyệt:

```jsx
// Hiển thị thông báo "Cửa hàng của bạn đang chờ Admin duyệt"
// + nút Logout
// + icon đồng hồ / trạng thái chờ
```

### [NEW] `src/pages/common/StoreBlocked.jsx`

Trang hiển thị khi store bị từ chối / khóa:

```jsx
// Hiển thị thông báo "Cửa hàng của bạn đã bị từ chối hoặc khóa"
// + nút Logout
// + hướng dẫn liên hệ admin
```

---

### [MODIFY] [Onboarding.jsx](file:///Users/Study/DOAN/z%20pos-source-code_1/pos-frontend-vite/src/pages/onboarding/Onboarding.jsx)

Sửa `useEffect` kiểm tra store (dòng 34–68):

```js
// TRƯỚC — chỉ check store.id có tồn tại
if (storeRes && storeRes.id) {
    navigate('/store');
}

// SAU — check cả status
if (storeRes && storeRes.id) {
    if (storeRes.status === 'ACTIVE') {
        navigate('/store');
    } else if (storeRes.status === 'PENDING') {
        navigate('/pending');
    } else if (storeRes.status === 'BLOCKED') {
        navigate('/blocked');
    }
}
```

Và catch error từ `getStoreByAdmin` khi backend ném exception:

```js
catch (err) {
    if (err?.includes?.('STORE_PENDING') || err?.message?.includes?.('STORE_PENDING')) {
        navigate('/pending');
        return;
    }
    if (err?.includes?.('STORE_BLOCKED') || err?.message?.includes?.('STORE_BLOCKED')) {
        navigate('/blocked');
        return;
    }
    // Không có store → ở lại step 2
    setStep(2);
}
```

---

### [MODIFY] [App.jsx](file:///Users/Study/DOAN/z%20pos-source-code_1/pos-frontend-vite/src/App.jsx)

Thêm route cho 2 trang mới vào nhánh `ROLE_STORE_ADMIN`:

```jsx
// TRƯỚC
if (!store) {
    content = <Routes><Route path="/auth/onboarding" .../></Routes>;
    return content;
}

// SAU — thêm route /pending và /blocked
content = (
    <Routes>
        <Route path="/auth/onboarding" element={<Onboarding />} />
        <Route path="/pending" element={<StorePending />} />
        <Route path="/blocked" element={<StoreBlocked />} />
        <Route path="*" element={<PageNotFound />} />
    </Routes>
);
```

Và với store đã load, vẫn guard theo status:

```jsx
} else {
    // Store đã có
    if (store.status === 'ACTIVE') {
        content = <Routes><Route path="/store/*" .../></Routes>;
    } else if (store.status === 'PENDING') {
        content = <Routes><Route path="*" element={<Navigate to="/pending" />}/></Routes>;
    } else if (store.status === 'BLOCKED') {
        content = <Routes><Route path="*" element={<Navigate to="/blocked" />}/></Routes>;
    }
}
```

---

## Tóm tắt các file cần thay đổi

| File | Loại | Mô tả |
|---|---|---|
| `StoreServiceImpl.java` | MODIFY | Thêm check status khi `getStoreByAdminId()` |
| `Onboarding.jsx` | MODIFY | Check `store.status` thay vì chỉ check `store.id` |
| `App.jsx` | MODIFY | Thêm route `/pending`, `/blocked`; guard route `/store` theo status |
| `StorePending.jsx` | NEW | Trang "Cửa hàng đang chờ duyệt" |
| `StoreBlocked.jsx` | NEW | Trang "Cửa hàng bị từ chối / khóa" |

## Kế hoạch kiểm tra

1. Đăng ký tài khoản mới → tạo store → đăng nhập lại → phải thấy trang **Pending**
2. Super Admin approve → đăng nhập lại → phải vào được `/store`
3. Super Admin block → đăng nhập lại → phải thấy trang **Blocked**
4. User bị block truy cập thẳng URL `/store` → phải bị redirect về `/blocked`

## Open Questions

> [!IMPORTANT]
> Bạn có muốn **gửi email thông báo** khi Super Admin approve/reject không? Nếu có cần thêm logic ở `moderateStore()` backend để gọi `EmailService`.

> [!NOTE]
> Hiện hệ thống dùng `BLOCKED` cho cả "từ chối lần đầu" và "khóa tài khoản đang hoạt động". Có nên tách thành `REJECTED` và `BLOCKED` riêng không? Nếu không thì dùng chung `BLOCKED` cũng được.
