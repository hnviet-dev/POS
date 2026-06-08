package com.zosh.controller;

import com.zosh.service.QrPaymentSessionService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * API cho frontend tương tác với QR payment sessions.
 *
 * Endpoints:
 *  POST /api/qr-payments/register  → đăng ký session khi hiển thị QR
 *  GET  /api/qr-payments/status/{ref} → frontend poll mỗi 3 giây
 *  DELETE /api/qr-payments/{ref}   → xóa session sau khi tạo order xong
 */
@RestController
@RequestMapping("/api/qr-payments")
@RequiredArgsConstructor
@Slf4j
public class QrPaymentController {

    private final QrPaymentSessionService qrPaymentSessionService;

    /**
     * Frontend gọi khi hiển thị QR để backend theo dõi.
     * Body: { "orderRef": "DH1234567", "amount": 372000 }
     */
    @PostMapping("/register")
    public ResponseEntity<Map<String, Object>> registerSession(
            @RequestBody Map<String, Object> body
    ) {
        String orderRef = (String) body.get("orderRef");
        Number amountNum = (Number) body.get("amount");

        if (orderRef == null || orderRef.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("success", false, "message", "orderRef is required"));
        }
        if (amountNum == null || amountNum.longValue() <= 0) {
            return ResponseEntity.badRequest().body(Map.of("success", false, "message", "amount must be > 0"));
        }

        qrPaymentSessionService.registerSession(orderRef.toUpperCase(), amountNum.longValue());
        log.info("📋 Registered QR session: ref={}, amount={}", orderRef, amountNum.longValue());

        return ResponseEntity.ok(Map.of(
                "success", true,
                "orderRef", orderRef.toUpperCase(),
                "message", "Session registered. Waiting for payment..."
        ));
    }

    /**
     * Frontend polling mỗi 3 giây khi QR đang hiển thị.
     * Response: { "status": "PENDING" | "PAID" | "NOT_FOUND" }
     */
    @GetMapping("/status/{orderRef}")
    public ResponseEntity<Map<String, Object>> checkStatus(@PathVariable String orderRef) {
        String status = qrPaymentSessionService.checkStatus(orderRef.toUpperCase());
        return ResponseEntity.ok(Map.of(
                "orderRef", orderRef.toUpperCase(),
                "status", status
        ));
    }

    /**
     * Frontend gọi sau khi tạo order thành công để cleanup session.
     */
    @DeleteMapping("/{orderRef}")
    public ResponseEntity<Void> removeSession(@PathVariable String orderRef) {
        qrPaymentSessionService.removeSession(orderRef.toUpperCase());
        return ResponseEntity.noContent().build();
    }
}
