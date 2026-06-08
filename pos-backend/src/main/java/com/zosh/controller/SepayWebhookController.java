package com.zosh.controller;

import com.zosh.service.QrPaymentSessionService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * Webhook endpoint nhận notification từ SePay khi có giao dịch ngân hàng.
 *
 * SePay gọi POST này mỗi khi có giao dịch vào tài khoản đã kết nối.
 * Docs: https://docs.sepay.vn/webhook.html
 *
 * Để cấu hình SePay:
 *  1. Đăng ký tài khoản tại sepay.vn
 *  2. Kết nối tài khoản ngân hàng
 *  3. Vào Webhook → thêm URL: https://your-domain.com/api/webhook/sepay
 *  4. Lấy API key để xác thực
 */
@RestController
@RequestMapping("/api/webhook")
@RequiredArgsConstructor
@Slf4j
public class SepayWebhookController {

    private final QrPaymentSessionService qrPaymentSessionService;

    // Thay bằng API key thực từ dashboard SePay
    private static final String SEPAY_API_KEY = "YOUR_SEPAY_API_KEY";

    /**
     * SePay gọi endpoint này khi có giao dịch.
     * Payload mẫu từ SePay:
     * {
     *   "id": 12345,
     *   "gateway": "MB Bank",
     *   "transactionDate": "2024-01-01 10:00:00",
     *   "accountNumber": "9999999998628",
     *   "content": "DH1234567 thanh toan",   ← nội dung chuyển khoản
     *   "transferAmount": 372000,
     *   "transferType": "in",                ← "in" = tiền vào, "out" = tiền ra
     *   "referenceCode": "FT24001...",
     *   "description": "..."
     * }
     */
    @PostMapping("/sepay")
    public ResponseEntity<Map<String, Object>> handleSepayWebhook(
            @RequestBody Map<String, Object> payload,
            @RequestHeader(value = "Authorization", required = false) String authHeader
    ) {
        log.info("📥 SePay webhook received: {}", payload);

        // ── 1. Xác thực API key (bật lên khi deploy thật) ──────────
        // Uncomment khi có API key thực:
        // if (!("Apikey " + SEPAY_API_KEY).equals(authHeader)) {
        //     log.warn("⚠️ Invalid SePay API key");
        //     return ResponseEntity.status(401).body(Map.of("success", false, "message", "Unauthorized"));
        // }

        // ── 2. Chỉ xử lý giao dịch tiền VÀO ───────────────────────
        String transferType = (String) payload.get("transferType");
        if (!"in".equalsIgnoreCase(transferType)) {
            log.info("⏭ Bỏ qua giao dịch ra: {}", transferType);
            return ResponseEntity.ok(Map.of("success", true, "message", "Ignored outbound"));
        }

        // ── 3. Trích xuất nội dung chuyển khoản và số tiền ─────────
        String content = (String) payload.getOrDefault("content", "");
        Number amountRaw = (Number) payload.getOrDefault("transferAmount", 0);
        long amount = amountRaw.longValue();

        log.info("💰 Giao dịch vào - nội dung: '{}', số tiền: {}", content, amount);

        // ── 4. Tìm mã đơn hàng trong nội dung CK (dạng DHxxxxxxx) ──
        String orderRef = qrPaymentSessionService.extractOrderRef(content);
        if (orderRef == null) {
            log.warn("⚠️ Không tìm thấy mã đơn hàng trong nội dung: '{}'", content);
            return ResponseEntity.ok(Map.of("success", true, "message", "No order ref found"));
        }

        log.info("🎯 Tìm thấy mã đơn hàng: {}", orderRef);

        // ── 5. Xác nhận thanh toán ──────────────────────────────────
        boolean confirmed = qrPaymentSessionService.confirmPayment(orderRef, amount);

        if (confirmed) {
            log.info("✅ Thanh toán xác nhận thành công cho đơn: {}", orderRef);
            return ResponseEntity.ok(Map.of("success", true, "message", "Payment confirmed", "orderRef", orderRef));
        } else {
            log.warn("❌ Xác nhận thất bại cho đơn: {} (không tìm thấy session hoặc số tiền sai)", orderRef);
            return ResponseEntity.ok(Map.of("success", false, "message", "Session not found or amount mismatch"));
        }
    }

    /**
     * Endpoint DEMO: Giả lập thanh toán thành công (dùng để test/demo).
     * Gọi: POST /api/webhook/simulate/{orderRef}
     * Dùng trong demo đồ án để minh họa luồng tự động.
     */
    @PostMapping("/simulate/{orderRef}")
    public ResponseEntity<Map<String, Object>> simulatePayment(@PathVariable String orderRef) {
        log.info("🎭 SIMULATE payment for orderRef: {}", orderRef);
        boolean confirmed = qrPaymentSessionService.confirmPaymentSimulate(orderRef);
        if (confirmed) {
            return ResponseEntity.ok(Map.of("success", true, "message", "Simulated payment confirmed", "orderRef", orderRef));
        }
        return ResponseEntity.badRequest().body(Map.of("success", false, "message", "Session not found: " + orderRef));
    }
}
