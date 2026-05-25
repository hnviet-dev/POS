# 🚀 HƯỚNG DẪN SETUP & DEMO — HỆ THỐNG POS (Zosh POS)
### 💻 Dành riêng cho MacBook Pro M1 (Apple Silicon)

> Tài liệu này hướng dẫn **toàn bộ các bước** cài đặt, cấu hình, build và chạy dự án POS System cho mục đích demo.
> Bao gồm cả **Backend (Spring Boot)** và **Frontend (React + Vite)**.

---

## 📊 TÌNH TRẠNG MÁY HIỆN TẠI

> Đã kiểm tra thực tế ngày 25/04/2026

| Công cụ | Tình trạng | Ghi chú |
|---------|-----------|---------|
| Java | ✅ **21.0.2 LTS** | Đủ dùng — xem giải thích bên dưới |
| Node.js | ✅ **v18.20.5** | OK |
| Homebrew | ✅ **5.0.5** | Dùng để cài các thứ còn lại |
| pnpm | ❌ Chưa cài | Cần cài ngay |
| MySQL | ❌ Chưa cài | Cần cài hoặc dùng Homebrew |
| Maven | Dùng wrapper `./mvnw` | Có sẵn trong project, không cần cài |

---

## 📌 MỤC LỤC

1. [Tổng quan kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Java 21 vs Java 17 — Dùng được không?](#2-java-21-vs-java-17--dùng-được-không)
3. [Cài pnpm](#3-cài-pnpm)
4. [Cài và setup MySQL trên M1](#4-cài-và-setup-mysql-trên-m1)
5. [Setup Backend (Spring Boot)](#5-setup-backend-spring-boot)
6. [Setup Frontend (React + Vite)](#6-setup-frontend-react--vite)
7. [Các dịch vụ bên thứ ba](#7-các-dịch-vụ-bên-thứ-ba)
8. [Chạy toàn bộ hệ thống để demo](#8-chạy-toàn-bộ-hệ-thống-để-demo)
9. [Tài khoản & Phân quyền](#9-tài-khoản--phân-quyền)
10. [Luồng demo khuyến nghị](#10-luồng-demo-khuyến-nghị)
11. [Xử lý lỗi thường gặp trên M1](#11-xử-lý-lỗi-thường-gặp-trên-m1)

---

## 1. Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────────┐
│                        HỆ THỐNG POS                         │
├──────────────────────┬──────────────────────────────────────┤
│      FRONTEND        │           BACKEND                    │
│  React 19 + Vite 7   │      Spring Boot 3.5.3               │
│  Redux Toolkit       │      Java 17+ (đang dùng 21 ✅)      │
│  TailwindCSS 4       │      Spring Security + JWT           │
│  shadcn/ui           │      Spring Data JPA (Hibernate)     │
│  Port: 5173          │      Port: 5000                      │
├──────────────────────┴──────────────────────────────────────┤
│                    DATABASE                                  │
│              MySQL 8.0  —  Port: 3306                       │
│                  Database name: pos                         │
├──────────────────────────────────────────────────────────────┤
│                 DỊCH VỤ BÊN THỨ BA                          │
│  Cloudinary (ảnh) │ Stripe (thanh toán) │ Gmail SMTP (mail)│
└──────────────────────────────────────────────────────────────┘
```

---

## 2. Java 21 vs Java 17 — Dùng được không?

> ✅ **Câu trả lời: DÙNG ĐƯỢC, không cần cài lại Java.**

**Lý do:**
- `pom.xml` khai báo `<java.version>17</java.version>` — đây là **phiên bản tối thiểu**, không phải phiên bản bắt buộc chính xác.
- **Spring Boot 3.5.3 hỗ trợ Java 17, 21, và 23** — Java 21 thậm chí là phiên bản LTS mới nhất được khuyến nghị.
- Java có tính **tương thích ngược** — code viết cho Java 17 chạy tốt trên Java 21.
- **Java 21 có native support tốt hơn cho Apple Silicon (M1/M2/M3).**

> Bạn đang dùng `Java HotSpot 64-Bit Server VM` — đây là **JVM chính thức của Oracle**, hoạt động tốt trên M1.

**Không cần làm gì thêm với Java.** ✅

---

## 3. Cài pnpm

pnpm là package manager dùng cho Frontend. Cài qua npm:

```bash
npm install -g pnpm
```

Kiểm tra:
```bash
pnpm --version
# Phải hiện: 8.x.x hoặc 9.x.x
```

---

## 4. Cài và setup MySQL trên M1

### Phương án A — Dùng Homebrew (Khuyến nghị cho M1 Mac)

Homebrew đã cài sẵn (v5.0.5). Chạy:

```bash
# Cài MySQL 8.0
brew install mysql@8.0

# Thêm mysql vào PATH (quan trọng trên M1!)
echo 'export PATH="/opt/homebrew/opt/mysql@8.0/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Khởi động MySQL service
brew services start mysql@8.0

# Kiểm tra đã chạy chưa
brew services list | grep mysql
# Phải thấy: mysql@8.0    started
```

> ⚠️ **Lưu ý M1:** Homebrew cài vào `/opt/homebrew/` (không phải `/usr/local/` như Intel Mac). Đường dẫn PATH phải là `/opt/homebrew/opt/mysql@8.0/bin`.

### Cài MySQL Workbench (GUI — Tùy chọn nhưng khuyến nghị)

Tải bản ARM64 tại: https://dev.mysql.com/downloads/workbench/

> Chọn macOS, bản **ARM** khi download.

### Đặt mật khẩu root MySQL

Sau khi cài, MySQL chạy **không có mật khẩu root** mặc định. Cần thiết lập:

```bash
# Chạy script bảo mật
mysql_secure_installation
```

Hoặc kết nối trực tiếp và đặt password:
```bash
# Kết nối MySQL (lần đầu không cần password)
mysql -u root

# Trong MySQL shell, đặt password
ALTER USER 'root'@'localhost' IDENTIFIED BY 'yourpassword';
FLUSH PRIVILEGES;
EXIT;
```

### Tạo database

```bash
# Kết nối MySQL
mysql -u root -p
# Nhập password khi được hỏi
```

```sql
-- Tạo database
CREATE DATABASE pos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Kiểm tra đã tạo chưa
SHOW DATABASES;

EXIT;
```

### Phương án B — Dùng Docker (Nếu đã cài Docker Desktop for Mac ARM)

```bash
docker run -d \
  --name pos-mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=pos \
  -p 3306:3306 \
  --platform linux/amd64 \
  mysql:8.0
```

> **Lưu ý M1:** Thêm `--platform linux/amd64` nếu MySQL image chưa có bản ARM native. Docker Desktop on M1 hỗ trợ emulation.

---

## 5. Setup Backend (Spring Boot)

### 5.1. Cấu hình `application.yml`

Mở file:
```
pos-backend/src/main/resources/application.yml
```

Phần **bắt buộc** phải chỉnh (database):

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/pos
    username: root
    password: yourpassword    # ← Sửa thành password MySQL bạn vừa đặt
```

Phần **không cần thiết cho demo cơ bản** (có thể để nguyên):

```yaml
  mail:
    username: your email      # ← Chỉ cần nếu demo chức năng quên mật khẩu
    password: your gmail app password

stripe:
  api:
    key: provide your stripe api key    # ← Chỉ cần nếu demo thanh toán Stripe

gemini:
  api:
    key: provide your gemin api key     # ← Tùy chọn, có thể bỏ qua
```

> **Tóm lại cho demo nhanh: chỉ cần sửa `password` trong phần `datasource`.**

### 5.2. Cấp quyền chạy cho `mvnw` (Chỉ làm 1 lần)

```bash
cd "/Users/Study/DOAN/z pos-source-code_1/pos-backend"
chmod +x mvnw
```

### 5.3. Chạy Backend

```bash
cd "/Users/Study/DOAN/z pos-source-code_1/pos-backend"
./mvnw spring-boot:run
```

**Lần đầu chạy sẽ:**
1. Download dependencies từ Maven Central (~2-5 phút, tùy tốc độ mạng)
2. Compile toàn bộ source Java
3. Kết nối MySQL và tự động tạo tất cả các bảng (nhờ `ddl-auto: update`)
4. Khởi động server trên port **5000**

**Dấu hiệu Backend đã sẵn sàng** — log terminal hiện:
```
Started PosSystemApplication in X.XXX seconds
Tomcat started on port 5000
```

### 5.4. Kiểm tra Backend hoạt động

```bash
curl http://localhost:5000/
```

Nếu nhận được response (kể cả `401 Unauthorized`) → Backend đang chạy ✅

### 5.5. Vấn đề Java version trong pom.xml (cần lưu ý)

File `pom.xml` khai báo `<java.version>17</java.version>`. Trên Java 21, Maven có thể hiện warning:

```
[WARNING] Using platform encoding (UTF-8 actually) to copy filtered resources...
```

**Đây là warning bình thường, không phải lỗi.** Build vẫn thành công. Nếu muốn bỏ warning, có thể sửa `pom.xml`:

```xml
<properties>
    <java.version>21</java.version>   <!-- Đổi từ 17 → 21 -->
</properties>
```

> Tuy nhiên **không bắt buộc** — project vẫn build và chạy tốt với Java 21 khi giữ nguyên `17`.

---

## 6. Setup Frontend (React + Vite)

### 6.1. Cài pnpm và dependencies

```bash
# Cài pnpm (nếu chưa có)
npm install -g pnpm

# Di chuyển vào thư mục frontend
cd "/Users/Study/DOAN/z pos-source-code_1/pos-frontend-vite"

# Cài đặt tất cả dependencies
pnpm install
```

> **Lần đầu `pnpm install`** sẽ download khoảng 500MB+ packages. Cần kết nối internet ổn định và chờ 2-5 phút.

### 6.2. Kiểm tra cấu hình API URL

Mở file `src/utils/api.js` — đảm bảo trỏ đúng Backend:

```javascript
const api = axios.create({
  baseURL: 'http://localhost:5000',   // ← Đúng rồi, không cần sửa
});
```

### 6.3. Chạy Frontend

```bash
cd "/Users/Study/DOAN/z pos-source-code_1/pos-frontend-vite"
pnpm dev
```

Terminal hiện:
```
  VITE v7.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

Mở browser → **http://localhost:5173/**

---

## 7. Các dịch vụ bên thứ ba

### Cloudinary (Upload ảnh) — Đã cấu hình sẵn ✅

Không cần làm gì. Đã có sẵn trong code:
- Cloud: `dxoqwusir`  
- Preset: `ml_default`

### Stripe, Gmail, Razorpay

Không cần thiết cho demo cơ bản (bán hàng tiền mặt, quản lý sản phẩm, báo cáo).
Chỉ cần nếu demo chức năng thanh toán online hoặc email.

---

## 8. Chạy toàn bộ hệ thống để demo

### Thứ tự khởi động (QUAN TRỌNG!)

```
Bước 1: Khởi động MySQL
    ↓
Bước 2: Khởi động Backend (chờ log "Started PosSystemApplication")
    ↓
Bước 3: Khởi động Frontend → mở http://localhost:5173
```

### Lệnh cụ thể — Mở 2 cửa sổ Terminal

**Terminal 1 — Khởi động MySQL (nếu chưa chạy):**
```bash
brew services start mysql@8.0
```

**Terminal 2 — Backend:**
```bash
cd "/Users/Study/DOAN/z pos-source-code_1/pos-backend"
./mvnw spring-boot:run
```

**Terminal 3 — Frontend:**
```bash
cd "/Users/Study/DOAN/z pos-source-code_1/pos-frontend-vite"
pnpm dev
```

### Bảng kiểm tra hệ thống

| Service | URL / Lệnh kiểm tra | Kết quả mong đợi |
|---------|---------------------|-----------------|
| MySQL | `brew services list \| grep mysql` | `started` |
| Backend | `curl http://localhost:5000/` | Trả về response bất kỳ |
| Frontend | http://localhost:5173 | Hiện trang Landing |

---

## 9. Tài khoản & Phân quyền

> ⚠️ **Database trống khi chạy lần đầu.** Phải tạo tài khoản Admin trước.

### Tạo Super Admin đầu tiên

```bash
curl -X POST http://localhost:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Super Admin",
    "email": "admin@pos.com",
    "password": "123456",
    "role": "ROLE_ADMIN"
  }'
```

### Đăng nhập (lấy JWT token)

```bash
curl -X POST http://localhost:5000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@pos.com",
    "password": "123456"
  }'
```

### Phân cấp người dùng

| Role | Dashboard URL | Mô tả |
|------|--------------|-------|
| `ROLE_ADMIN` | `/super-admin` | Quản lý toàn hệ thống |
| `ROLE_STORE_ADMIN` | `/store` | Quản lý cửa hàng |
| `ROLE_STORE_MANAGER` | `/store` | Nhân viên quản lý cửa hàng |
| `ROLE_BRANCH_ADMIN` | `/branch` | Quản lý chi nhánh |
| `ROLE_BRANCH_MANAGER` | `/branch` | Nhân viên chi nhánh |
| `ROLE_BRANCH_CASHIER` | `/cashier` | Thu ngân POS |

### Luồng tạo hệ thống phân cấp

```
1. Tạo Super Admin (qua curl/Postman)
2. Super Admin đăng nhập → /super-admin → Tạo Store Admin
3. Store Admin đăng nhập → Onboarding (tạo Store)
4. Store Admin tạo Branch và nhân viên
5. Cashier đăng nhập → Màn hình POS
```

---

## 10. Luồng demo khuyến nghị

### Kịch bản demo 10 phút

| Thời gian | Chức năng | URL |
|-----------|-----------|-----|
| 0-2 phút | Đăng nhập Store Admin, xem Dashboard tổng quan | `/store` |
| 2-4 phút | Quản lý sản phẩm — thêm mới, upload ảnh | `/store/products` |
| 4-6 phút | Màn hình POS (Cashier) — thêm giỏ, thanh toán tiền mặt | `/cashier` |
| 6-8 phút | Quản lý kho Inventory | `/store/inventory` |
| 8-10 phút | Báo cáo & Analytics, biểu đồ doanh thu | `/store/analytics` |

### Các URL quan trọng

| Trang | URL |
|-------|-----|
| Landing | http://localhost:5173/ |
| Đăng nhập | http://localhost:5173/auth/login |
| Super Admin | http://localhost:5173/super-admin |
| Store Dashboard | http://localhost:5173/store |
| Branch Dashboard | http://localhost:5173/branch |
| Cashier POS | http://localhost:5173/cashier |

---

## 11. Xử lý lỗi thường gặp trên M1

### ❌ `zsh: command not found: mysql`

MySQL chưa được thêm vào PATH. Chạy:
```bash
echo 'export PATH="/opt/homebrew/opt/mysql@8.0/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

### ❌ `Access denied for user 'root'@'localhost'`

Sai password MySQL. Kiểm tra lại password bạn đã đặt và sửa trong `application.yml`:
```yaml
spring:
  datasource:
    password: your_actual_mysql_password
```

---

### ❌ `Communications link failure` / `Cannot connect to MySQL`

MySQL chưa chạy. Khởi động lại:
```bash
brew services restart mysql@8.0
brew services list | grep mysql   # Kiểm tra status
```

---

### ❌ Backend lỗi `Error creating bean with name 'entityManagerFactory'`

Database chưa tồn tại. Tạo database:
```bash
mysql -u root -p -e "CREATE DATABASE pos CHARACTER SET utf8mb4;"
```

---

### ❌ `./mvnw: Permission denied`

```bash
chmod +x "/Users/Study/DOAN/z pos-source-code_1/pos-backend/mvnw"
```

---

### ❌ `pnpm: command not found`

```bash
npm install -g pnpm
```

---

### ❌ Frontend lỗi CORS khi gọi API

Đảm bảo Backend đang chạy trên port **5000** và Frontend trên port **5173** (đã cấu hình sẵn trong `SecurityConfig.java`).

---

### ❌ Lỗi `illegal reflective access` hoặc warning Java modules

Đây là warning bình thường khi chạy Spring Boot trên Java 21. Không ảnh hưởng đến hoạt động. Bỏ qua.

---

## ✅ CHECKLIST SETUP ĐẦY ĐỦ (M1 Mac)

```
[✅] Java 21 — Đã có, đủ dùng
[✅] Node.js 18.20.5 — Đã có
[✅] Homebrew 5.0.5 — Đã có

[ ] Cài pnpm:       npm install -g pnpm
[ ] Cài MySQL:      brew install mysql@8.0
[ ] Thêm PATH:      echo 'export PATH="/opt/homebrew/opt/mysql@8.0/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
[ ] Start MySQL:    brew services start mysql@8.0
[ ] Tạo database:   mysql -u root -e "CREATE DATABASE pos CHARACTER SET utf8mb4;"
[ ] Sửa application.yml — đặt đúng password MySQL
[ ] chmod +x mvnw

[ ] Terminal 1: ./mvnw spring-boot:run (chờ "Started PosSystemApplication")
[ ] Terminal 2: pnpm install && pnpm dev

[ ] Tạo Super Admin: curl POST /auth/signup
[ ] Mở http://localhost:5173 → Đăng nhập → Demo!
```

---

*Dự án POS System — Đồ án tốt nghiệp*
*Stack: Spring Boot 3.5.3 + Java 17/21 | React 19 + Vite 7 | MySQL 8.0*
*Máy: MacBook Pro M1 (Apple Silicon) — macOS*
