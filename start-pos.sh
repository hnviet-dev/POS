#!/bin/bash
# ============================================
#  SCRIPT KHỞI ĐỘNG HỆ THỐNG POS ĐA CHI NHÁNH
#  Chạy: bash start-pos.sh
# bash "/Users/Study/DOAN/z pos-source-code_1/start-pos.sh"

# ============================================

ROOT="/Users/Study/DOAN/z pos-source-code_1"
BACKEND="$ROOT/pos-backend"
FRONTEND="$ROOT/pos-frontend-vite"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║     🚀 KHỞI ĐỘNG HỆ THỐNG POS        ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── BƯỚC 1: Kiểm tra XAMPP MySQL ──────────────────────
echo "📦 [1/3] Kiểm tra MySQL (XAMPP)..."
MYSQL_OK=$(/Applications/XAMPP/xamppfiles/bin/mysql -u root -e "USE pos;" 2>/dev/null && echo "ok" || echo "fail")

if [ "$MYSQL_OK" != "ok" ]; then
  echo ""
  echo "  ❌ MySQL chưa chạy!"
  echo "  👉 Mở XAMPP → bật MySQL → chạy lại script này."
  echo ""
  exit 1
fi
echo "  ✅ MySQL đang chạy, database 'pos' sẵn sàng."

# ── BƯỚC 2: Kill process cũ trên port 8080 & 5173 ─────
echo ""
echo "🔄 [2/3] Dọn dẹp port cũ..."
lsof -ti :8080 | xargs kill -9 2>/dev/null && echo "  ✅ Đã giải phóng port 8080" || echo "  ℹ️  Port 8080 đã trống"
lsof -ti :5173 | xargs kill -9 2>/dev/null && echo "  ✅ Đã giải phóng port 5173" || echo "  ℹ️  Port 5173 đã trống"
sleep 1

# ── BƯỚC 3: Khởi động Backend ─────────────────────────
echo ""
echo "☕ [3/3] Khởi động Backend Spring Boot..."
cd "$BACKEND"
./mvnw spring-boot:run -q > /tmp/pos-backend.log 2>&1 &
BE_PID=$!
echo "  Backend PID: $BE_PID"

# Chờ backend sẵn sàng
echo "  ⏳ Đang chờ backend khởi động"
for i in {1..30}; do
  sleep 2
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/auth/login \
    -X POST -H "Content-Type: application/json" \
    -d '{"email":"x","password":"x"}' 2>/dev/null)
  if [ "$STATUS" = "400" ] || [ "$STATUS" = "200" ] || [ "$STATUS" = "401" ]; then
    echo "  ✅ Backend đã sẵn sàng! (${i}x2 giây)"
    break
  fi
  echo -n "."
done
echo ""

# ── BƯỚC 4: Khởi động Frontend ────────────────────────
echo "⚛️  [4/4] Khởi động Frontend React + Vite..."
cd "$FRONTEND"
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
nvm use 22 --silent 2>/dev/null
npm run dev > /tmp/pos-frontend.log 2>&1 &
FE_PID=$!
echo "  Frontend PID: $FE_PID"

# Chờ frontend sẵn sàng
sleep 5
FE_STATUS=$(grep -c "Local:" /tmp/pos-frontend.log 2>/dev/null || echo 0)
if [ "$FE_STATUS" -ge "1" ]; then
  echo "  ✅ Frontend đã sẵn sàng!"
else
  echo "  ⚠️  Frontend đang khởi động, vui lòng chờ thêm..."
fi

# ── TỔNG KẾT ──────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║          ✅ HỆ THỐNG POS ĐÃ SẴN SÀNG!           ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  🌐 Frontend :  http://localhost:5173            ║"
echo "║  ⚙️  Backend  :  http://localhost:8080            ║"
echo "║  🗄️  Database :  localhost:3306  (DB: pos)       ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  🔑 Super Admin: codewithzosh@gmail.com          ║"
echo "║  🔑 Password   : codewithzosh                    ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  📋 Log Backend : tail -f /tmp/pos-backend.log   ║"
echo "║  📋 Log Frontend: tail -f /tmp/pos-frontend.log  ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  ❌ Dừng hệ thống: bash stop-pos.sh              ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Mở trình duyệt tự động
sleep 2
open http://localhost:5173
