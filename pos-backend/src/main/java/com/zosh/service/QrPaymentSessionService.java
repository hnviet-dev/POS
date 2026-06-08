package com.zosh.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Service quản lý các phiên thanh toán QR đang chờ xác nhận.
 *
 * Dùng ConcurrentHashMap để lưu in-memory (đủ cho đồ án).
 * Trong production, nên chuyển sang Redis hoặc DB table.
 *
 * Flow:
 *  1. Frontend gọi registerSession(ref, amount) khi hiển thị QR
 *  2. SePay webhook gọi confirmPayment(ref, amount) khi nhận tiền
 *  3. Frontend polling checkStatus(ref) để biết đã nhận tiền chưa
 */
@Service
@Slf4j
public class QrPaymentSessionService {

    // Key = orderRef (e.g. "DH1234567"), Value = session data
    private final Map<String, QrSession> sessions = new ConcurrentHashMap<>();

    // Regex tìm mã DH trong nội dung chuyển khoản
    private static final Pattern ORDER_REF_PATTERN = Pattern.compile("\\bDH\\d{5,10}\\b", Pattern.CASE_INSENSITIVE);

    // Tự xóa session sau 30 phút để tránh memory leak
    private static final long SESSION_TTL_MINUTES = 30;

    // ── Public API ──────────────────────────────────────────────────

    /**
     * Đăng ký phiên QR mới khi cashier mở dialog thanh toán QR.
     * @param orderRef  mã đơn hàng, VD: "DH1234567"
     * @param amount    số tiền cần thu (VND)
     */
    public void registerSession(String orderRef, long amount) {
        sessions.put(orderRef, new QrSession(orderRef, amount));
        log.info("📋 QR Session registered: ref={}, amount={}", orderRef, amount);
        cleanExpiredSessions();
    }

    /**
     * Kiểm tra trạng thái phiên — frontend gọi mỗi 3 giây.
     * @return "PENDING" | "PAID" | "NOT_FOUND"
     */
    public String checkStatus(String orderRef) {
        QrSession session = sessions.get(orderRef);
        if (session == null) return "NOT_FOUND";
        return session.isPaid() ? "PAID" : "PENDING";
    }

    /**
     * SePay webhook gọi hàm này sau khi verify.
     * Xác nhận thanh toán nếu ref tồn tại và số tiền khớp (cho phép sai lệch 1000đ).
     */
    public boolean confirmPayment(String orderRef, long receivedAmount) {
        QrSession session = sessions.get(orderRef);
        if (session == null) {
            log.warn("⚠️ Session not found for ref: {}", orderRef);
            return false;
        }
        if (session.isPaid()) {
            log.info("ℹ️ Session already paid: {}", orderRef);
            return true; // idempotent
        }

        // Cho phép chênh lệch ±1000đ (làm tròn)
        long diff = Math.abs(receivedAmount - session.getAmount());
        if (diff > 1000) {
            log.warn("💸 Amount mismatch for {}: expected={}, received={}", orderRef, session.getAmount(), receivedAmount);
            return false;
        }

        session.markPaid(receivedAmount);
        log.info("✅ Payment confirmed: ref={}, amount={}", orderRef, receivedAmount);
        return true;
    }

    /**
     * Giả lập thanh toán thành công (dùng cho demo/test).
     */
    public boolean confirmPaymentSimulate(String orderRef) {
        QrSession session = sessions.get(orderRef);
        if (session == null) {
            log.warn("⚠️ Simulate: session not found for {}", orderRef);
            return false;
        }
        session.markPaid(session.getAmount());
        log.info("🎭 Simulated payment confirmed: {}", orderRef);
        return true;
    }

    /**
     * Xóa session sau khi đơn hàng đã được tạo thành công.
     */
    public void removeSession(String orderRef) {
        sessions.remove(orderRef);
        log.info("🗑 Session removed: {}", orderRef);
    }

    /**
     * Kiểm tra có session nào đang PENDING không.
     * SepayPollingService dùng để quyết định có cần poll API không.
     */
    public boolean hasPendingSessions() {
        return sessions.values().stream().anyMatch(s -> !s.isPaid());
    }

    /**
     * Trích xuất mã DH từ nội dung chuyển khoản.
     * VD: "DH1234567 thanh toan tien hang" → "DH1234567"
     */
    public String extractOrderRef(String content) {
        if (content == null || content.isBlank()) return null;
        Matcher m = ORDER_REF_PATTERN.matcher(content);
        return m.find() ? m.group().toUpperCase() : null;
    }

    // ── Private helpers ──────────────────────────────────────────────

    private void cleanExpiredSessions() {
        LocalDateTime cutoff = LocalDateTime.now().minusMinutes(SESSION_TTL_MINUTES);
        sessions.entrySet().removeIf(entry -> entry.getValue().getCreatedAt().isBefore(cutoff));
    }

    // ── Inner class: session data ────────────────────────────────────

    public static class QrSession {
        private final String orderRef;
        private final long amount;
        private final LocalDateTime createdAt;
        private boolean paid = false;
        private long paidAmount = 0;
        private LocalDateTime paidAt;

        public QrSession(String orderRef, long amount) {
            this.orderRef = orderRef;
            this.amount = amount;
            this.createdAt = LocalDateTime.now();
        }

        public void markPaid(long paidAmount) {
            this.paid = true;
            this.paidAmount = paidAmount;
            this.paidAt = LocalDateTime.now();
        }

        public boolean isPaid() { return paid; }
        public long getAmount() { return amount; }
        public String getOrderRef() { return orderRef; }
        public LocalDateTime getCreatedAt() { return createdAt; }
        public long getPaidAmount() { return paidAmount; }
        public LocalDateTime getPaidAt() { return paidAt; }
    }
}
