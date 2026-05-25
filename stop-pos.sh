#!/bin/bash
# ============================================
#  SCRIPT DỪNG HỆ THỐNG POS
#  Chạy: bash stop-pos.sh
# ============================================

echo ""
echo "🛑 Đang dừng hệ thống POS..."
echo ""

lsof -ti :8080 | xargs kill -9 2>/dev/null && echo "  ✅ Đã dừng Backend  (port 8080)" || echo "  ℹ️  Backend không chạy"
lsof -ti :5173 | xargs kill -9 2>/dev/null && echo "  ✅ Đã dừng Frontend (port 5173)" || echo "  ℹ️  Frontend không chạy"

echo ""
echo "  ✅ Hệ thống POS đã dừng hoàn toàn."
echo "  💡 MySQL (XAMPP) vẫn đang chạy — tắt thủ công nếu cần."
echo ""
