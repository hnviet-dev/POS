package com.zosh.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

/**
 * Service tự động poll SePay Transaction API để phát hiện giao dịch.
 *
 * Cấu trúc JSON từ SePay (v1 API):
 * GET /userapi/transactions/list → { "transactions": [ { "transaction_content": "...", "amount_in": "18067000.00", ... } ] }
 *
 * Lưu ý quan trọng:
 *  - Key là "transactions" (số nhiều, array)
 *  - "amount_in" là STRING thập phân (VD: "18067000.00") → cần parse Double rồi chuyển sang long
 *  - "transaction_content" là nội dung chuyển khoản
 *  - Dùng "since_id" để chỉ lấy giao dịch mới, tránh re-process giao dịch cũ
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class SepayPollingService {

    private final QrPaymentSessionService qrPaymentSessionService;
    private final RestTemplate restTemplate;

    @Value("${sepay.api.token:}")
    private String sepayApiToken;

    // ID giao dịch cuối cùng đã xử lý — tránh re-process giao dịch cũ
    // Dùng since_id thay transaction_date_min: chính xác hơn, không bị lỗi timezone
    private volatile String lastSeenId = null;

    private static final String SEPAY_BASE_URL =
            "https://my.sepay.vn/userapi/transactions/list?limit=20";

    /**
     * Chạy mỗi 4 giây khi có ít nhất 1 session đang PENDING.
     * fixedDelay đảm bảo các lần gọi không chồng lên nhau.
     */
    @Scheduled(fixedDelay = 4000)
    public void pollTransactions() {
        if (sepayApiToken == null || sepayApiToken.isBlank()
                || sepayApiToken.equals("YOUR_SEPAY_API_TOKEN_HERE")) {
            return;
        }
        if (!qrPaymentSessionService.hasPendingSessions()) {
            return;
        }

        try {
            List<Map<String, Object>> transactions = fetchRecentTransactions();
            if (transactions == null || transactions.isEmpty()) return;

            for (Map<String, Object> txn : transactions) {
                processSingleTransaction(txn);
            }

            // Cập nhật lastSeenId từ giao dịch đầu tiên (mới nhất)
            if (!transactions.isEmpty()) {
                Object firstId = transactions.get(0).get("id");
                if (firstId != null) {
                    String newId = String.valueOf(firstId);
                    if (!newId.equals(lastSeenId)) {
                        log.debug("📌 Cập nhật lastSeenId: {} → {}", lastSeenId, newId);
                        lastSeenId = newId;
                    }
                }
            }
        } catch (Exception e) {
            log.warn("⚠️ SePay poll error: {}", e.getMessage());
        }
    }

    @SuppressWarnings("unchecked")
    private List<Map<String, Object>> fetchRecentTransactions() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + sepayApiToken);
        headers.setAccept(List.of(MediaType.APPLICATION_JSON));
        HttpEntity<Void> entity = new HttpEntity<>(headers);

        // Dùng since_id nếu đã biết ID cuối cùng, ngược lại lấy 20 giao dịch gần nhất
        String url;
        if (lastSeenId != null) {
            url = SEPAY_BASE_URL + "&since_id=" + lastSeenId;
        } else {
            // Lần đầu khởi động: chỉ lấy 20 giao dịch gần nhất để init lastSeenId
            url = SEPAY_BASE_URL;
        }

        log.debug("🔍 Poll SePay: {}", url);

        try {
            ResponseEntity<Map> response = restTemplate.exchange(
                    url, HttpMethod.GET, entity, Map.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                Map<String, Object> body = response.getBody();

                // Theo docs chính thức: key là "transactions" (array)
                Object txnObj = body.get("transactions");
                if (txnObj instanceof List) {
                    List<Map<String, Object>> list = (List<Map<String, Object>>) txnObj;

                    // Lần đầu: chỉ init lastSeenId, không process để tránh confirm giao dịch cũ
                    if (lastSeenId == null && !list.isEmpty()) {
                        Object firstId = list.get(0).get("id");
                        if (firstId != null) {
                            lastSeenId = String.valueOf(firstId);
                            log.info("📌 SePay polling khởi động. lastSeenId = {}", lastSeenId);
                        }
                        return List.of(); // Không process lần đầu
                    }

                    if (!list.isEmpty()) {
                        log.info("📊 SePay poll: {} giao dịch mới (since_id={})", list.size(), lastSeenId);
                    }
                    return list;
                }

                log.warn("⚠️ SePay response thiếu key 'transactions'. Keys có: {}", body.keySet());
            } else {
                log.warn("⚠️ SePay API status: {}", response.getStatusCode());
            }
        } catch (Exception e) {
            log.warn("⚠️ SePay API call failed: {}", e.getMessage());
        }
        return List.of();
    }

    private void processSingleTransaction(Map<String, Object> txn) {
        // Lấy nội dung chuyển khoản
        String content = String.valueOf(txn.getOrDefault("transaction_content", ""));
        if (content.isBlank() || content.equals("null")) return;

        // ── Lấy số tiền ────────────────────────────────────────────────
        // Theo docs: amount_in là STRING thập phân, VD: "18067000.00"
        // KHÔNG dùng Long.parseLong vì sẽ crash với "18067000.00"
        Object amtObj = txn.get("amount_in");
        long amount = 0;
        if (amtObj != null) {
            try {
                // parseDouble xử lý cả "18067000.00" lẫn số nguyên
                amount = (long) Double.parseDouble(String.valueOf(amtObj));
            } catch (NumberFormatException e) {
                log.warn("⚠️ Không parse được amount_in: '{}'", amtObj);
            }
        }

        // Tìm mã DH trong nội dung
        String orderRef = qrPaymentSessionService.extractOrderRef(content);
        if (orderRef == null) return;

        log.info("🎯 SePay - Tìm thấy mã: {} | nội dung: '{}' | số tiền: {}đ",
                orderRef, content, String.format("%,d", amount));

        // Xác nhận thanh toán
        boolean confirmed = qrPaymentSessionService.confirmPayment(orderRef, amount);
        if (confirmed) {
            log.info("✅ Auto-confirmed: ref={}, amount={}đ", orderRef, String.format("%,d", amount));
        }
    }
}
