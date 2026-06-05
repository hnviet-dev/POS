package com.zosh.service.impl;

import com.google.genai.Client;
import com.google.genai.types.GenerateContentResponse;
import com.zosh.exception.UserException;
import com.zosh.modal.User;
import com.zosh.repository.*;
import com.zosh.service.AiChatService;
import com.zosh.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

@Service
@Slf4j
public class AiChatServiceImpl implements AiChatService {

    private final UserService userService;
    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;
    private final BranchRepository branchRepository;
    private final InventoryRepository inventoryRepository;
    private final RefundRepository refundRepository;
    private final UserRepository userRepository;
    private final CustomerRepository customerRepository;

    private final Client geminiClient;
    private final String geminiApiKey;

    private static final String MODEL = "gemini-2.5-flash";

    public AiChatServiceImpl(
            UserService userService,
            OrderRepository orderRepository,
            ProductRepository productRepository,
            BranchRepository branchRepository,
            InventoryRepository inventoryRepository,
            RefundRepository refundRepository,
            UserRepository userRepository,
            CustomerRepository customerRepository,
            @Value("${gemini.api.key:}") String geminiApiKey) {
        this.userService = userService;
        this.orderRepository = orderRepository;
        this.productRepository = productRepository;
        this.branchRepository = branchRepository;
        this.inventoryRepository = inventoryRepository;
        this.refundRepository = refundRepository;
        this.userRepository = userRepository;
        this.customerRepository = customerRepository;
        this.geminiApiKey = geminiApiKey;

        // Khởi tạo Gemini client
        if (geminiApiKey != null && !geminiApiKey.isBlank()
                && !geminiApiKey.contains("provide") && !geminiApiKey.contains("optional")) {
            this.geminiClient = Client.builder().apiKey(geminiApiKey).build();
            log.info("✅ Gemini AI client initialized successfully");
        } else {
            this.geminiClient = null;
            log.warn("⚠️ Gemini API key not configured. AI features will use fallback mode.");
        }
    }

    // ──────────────────────────────────────────────
    // 1. CHAT — Trả lời câu hỏi tự nhiên
    // ──────────────────────────────────────────────
    @Override
    public String chat(String message, String jwt) throws UserException {
        User user = userService.getUserFromJwtToken(jwt);

        // Xây dựng context dựa trên role của user
        String context = buildContextForUser(user);

        String fullPrompt = """
                [SYSTEM]
                Bạn là trợ lý AI thông minh cho hệ thống quản lý bán hàng POS (Point of Sale).
                Tên bạn là "POS AI Assistant".

                NGUYÊN TẮC:
                - Trả lời bằng tiếng Việt, ngắn gọn, rõ ràng
                - Dùng emoji phù hợp để dễ đọc
                - Nếu có số liệu, trình bày dạng danh sách
                - Nếu không có dữ liệu, nói rõ "Chưa có dữ liệu"
                - Nếu câu hỏi không liên quan đến POS, lịch sự từ chối
                - Khi đưa ra nhận xét, hãy thêm gợi ý hành động cụ thể

                THÔNG TIN NGƯỜI DÙNG:
                - Tên: %s
                - Vai trò: %s
                - Cửa hàng: %s
                - Chi nhánh: %s

                DỮ LIỆU HỆ THỐNG HIỆN TẠI:
                %s

                [USER]
                %s
                """.formatted(
                user.getFullName(),
                user.getRole().name(),
                user.getStore() != null ? user.getStore().getBrand() : "N/A",
                user.getBranch() != null ? user.getBranch().getName() : "Tất cả chi nhánh",
                context,
                message);

        return callGemini(fullPrompt);
    }

    // ──────────────────────────────────────────────
    // 2. DASHBOARD INSIGHT — Tóm tắt thông minh
    // ──────────────────────────────────────────────
    @Override
    public String getDashboardInsight(String jwt) throws UserException {
        User user = userService.getUserFromJwtToken(jwt);
        String context = buildContextForUser(user);

        String prompt = """
                Dựa trên dữ liệu POS sau, hãy đưa ra BÁO CÁO NGẮN GỌN gồm:
                1. 📊 Tổng quan: 1-2 câu nhận xét tình hình chung
                2. 📈 Xu hướng: Doanh thu đang tăng hay giảm?
                3. ⚠️ Cảnh báo: Vấn đề cần chú ý (nếu có)
                4. 💡 Gợi ý: 1-2 hành động nên làm

                Trả lời ngắn gọn trong 4-5 dòng, dùng emoji, bằng tiếng Việt.

                DỮ LIỆU:
                %s
                """.formatted(context);

        return callGemini(prompt);
    }

    // ──────────────────────────────────────────────
    // 3. GỢI Ý CÂU HỎI NHANH
    // ──────────────────────────────────────────────
    @Override
    public List<String> getSuggestedQuestions() {
        return List.of(
                "Doanh thu hôm nay bao nhiêu?",
                "Sản phẩm nào bán chạy nhất?",
                "Chi nhánh nào có doanh thu cao nhất?",
                "Có sản phẩm nào sắp hết hàng không?",
                "So sánh doanh thu hôm nay với hôm qua",
                "Tổng số đơn hàng trong tuần này?",
                "Thu ngân nào bán được nhiều nhất?",
                "Tỷ lệ hoàn trả hiện tại là bao nhiêu?");
    }

    // ══════════════════════════════════════════════
    // PRIVATE METHODS
    // ══════════════════════════════════════════════

    /**
     * Xây dựng context dữ liệu dựa trên role của user.
     */
    private String buildContextForUser(User user) {
        StringBuilder ctx = new StringBuilder();

        try {
            if (user.getStore() != null) {
                Long storeId = user.getStore().getId();

                // --- TỔNG QUAN STORE ---
                long totalOrders = orderRepository.countByBranch_Store_Id(storeId);
                Double totalSales = orderRepository.sumTotalAmountByBranch_Store_Id(storeId);
                long totalProducts = productRepository.countByStoreId(storeId);
                long totalBranches = branchRepository.countByStoreId(storeId);
                long totalRefunds = refundRepository.countByBranch_Store_Id(storeId);

                ctx.append("=== TỔNG QUAN CỬA HÀNG ===\n");
                ctx.append("Tổng đơn hàng: ").append(totalOrders).append("\n");
                ctx.append("Tổng doanh thu: ").append(formatCurrency(totalSales)).append("\n");
                ctx.append("Tổng sản phẩm: ").append(totalProducts).append("\n");
                ctx.append("Tổng chi nhánh: ").append(totalBranches).append("\n");
                ctx.append("Tổng hoàn trả: ").append(totalRefunds).append("\n");

                // --- DOANH THU HÔM NAY ---
                LocalDateTime todayStart = LocalDate.now().atStartOfDay();
                LocalDateTime todayEnd = todayStart.plusDays(1);

                List<Object[]> todayStats = orderRepository
                        .countAndSumByStoreIdAndDateRange(storeId, todayStart, todayEnd);
                if (todayStats != null && !todayStats.isEmpty()) {
                    Object[] row = todayStats.get(0);
                    ctx.append("\n=== HÔM NAY (").append(LocalDate.now()).append(") ===\n");
                    ctx.append("Số đơn hôm nay: ").append(row[0] != null ? row[0] : 0).append("\n");
                    ctx.append("Doanh thu hôm nay: ")
                            .append(formatCurrency(row[1] != null ? ((Number) row[1]).doubleValue() : 0)).append("\n");
                }

                // --- DOANH THU HÔM QUA ---
                LocalDateTime yesterdayStart = todayStart.minusDays(1);
                List<Object[]> yesterdayStats = orderRepository
                        .countAndSumByStoreIdAndDateRange(storeId, yesterdayStart, todayStart);
                if (yesterdayStats != null && !yesterdayStats.isEmpty()) {
                    Object[] row = yesterdayStats.get(0);
                    ctx.append("\n=== HÔM QUA ===\n");
                    ctx.append("Số đơn hôm qua: ").append(row[0] != null ? row[0] : 0).append("\n");
                    ctx.append("Doanh thu hôm qua: ")
                            .append(formatCurrency(row[1] != null ? ((Number) row[1]).doubleValue() : 0)).append("\n");
                }

                // --- TOP SẢN PHẨM BÁN CHẠY ---
                List<Object[]> topProducts = orderRepository.findTopSellingProducts(storeId, 5);
                if (topProducts != null && !topProducts.isEmpty()) {
                    ctx.append("\n=== TOP 5 SẢN PHẨM BÁN CHẠY ===\n");
                    for (Object[] p : topProducts) {
                        ctx.append("- ").append(p[0]).append(": ")
                                .append(p[1]).append(" đơn, doanh thu ")
                                .append(formatCurrency(p[2] != null ? ((Number) p[2]).doubleValue() : 0))
                                .append("\n");
                    }
                }

                // --- DOANH THU THEO CHI NHÁNH ---
                List<Object[]> branchSales = orderRepository.findSalesByBranchForStore(storeId);
                if (branchSales != null && !branchSales.isEmpty()) {
                    ctx.append("\n=== DOANH THU THEO CHI NHÁNH ===\n");
                    for (Object[] b : branchSales) {
                        ctx.append("- ").append(b[0]).append(": ")
                                .append(b[1]).append(" đơn, ")
                                .append(formatCurrency(b[2] != null ? ((Number) b[2]).doubleValue() : 0))
                                .append("\n");
                    }
                }

                // --- TỒN KHO THẤP ---
                List<Object[]> lowStock = inventoryRepository.findLowStockItems(storeId, 10);
                if (lowStock != null && !lowStock.isEmpty()) {
                    ctx.append("\n=== SẢN PHẨM SẮP HẾT HÀNG (≤10) ===\n");
                    for (Object[] item : lowStock) {
                        ctx.append("- ").append(item[0]).append(" tại ").append(item[1])
                                .append(": còn ").append(item[2]).append(" sản phẩm\n");
                    }
                }

            } else if (user.getBranch() != null) {
                // Branch-level context
                Long branchId = user.getBranch().getId();
                ctx.append("=== CHI NHÁNH: ").append(user.getBranch().getName()).append(" ===\n");

                long branchOrders = orderRepository.countByBranchId(branchId);
                ctx.append("Tổng đơn hàng chi nhánh: ").append(branchOrders).append("\n");
            }
        } catch (Exception e) {
            log.warn("Error building AI context: {}", e.getMessage());
            ctx.append("Không thể tải đầy đủ dữ liệu hệ thống.\n");
        }

        return ctx.toString();
    }

    /**
     * Gọi Gemini API bằng SDK chính thức.
     */
    private String callGemini(String prompt) {
        if (geminiClient == null) {
            return getFallbackResponse(prompt);
        }

        try {
            GenerateContentResponse response = geminiClient.models.generateContent(
                    MODEL,
                    prompt,
                    null);

            String text = response.text();
            if (text != null && !text.isBlank()) {
                return text;
            }

            return "🤖 Không nhận được phản hồi từ AI. Vui lòng thử lại.";

        } catch (Exception e) {
            log.error("Gemini API error: {}", e.getMessage(), e);

            if (e.getMessage() != null && e.getMessage().contains("429")) {
                return "⏳ AI đang bận, vui lòng thử lại sau 30 giây.";
            }
            if (e.getMessage() != null && e.getMessage().contains("403")) {
                return "🔑 API key không hợp lệ. Vui lòng kiểm tra lại cấu hình.";
            }

            return "⚠️ Lỗi kết nối AI: " + e.getMessage();
        }
    }

    /**
     * Fallback khi không có API key.
     */
    private String getFallbackResponse(String message) {
        return "🤖 **POS AI Assistant**\n\n" +
                "Để sử dụng chatbot AI, bạn cần cấu hình Gemini API key.\n\n" +
                "**Hướng dẫn nhanh:**\n" +
                "1. Truy cập https://aistudio.google.com/apikey\n" +
                "2. Tạo API key miễn phí\n" +
                "3. Thêm vào `application.yml` → `gemini.api.key`\n" +
                "4. Khởi động lại backend\n\n" +
                "Chatbot sẽ hỗ trợ bạn tra cứu doanh thu, phân tích sản phẩm, cảnh báo tồn kho! 🚀";
    }

    private String formatCurrency(Double amount) {
        if (amount == null)
            return "$0";
        return String.format("$%,.0f", amount);
    }

    private String formatCurrency(double amount) {
        return String.format("$%,.0f", amount);
    }
}
