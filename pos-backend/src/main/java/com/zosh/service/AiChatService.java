package com.zosh.service;

import com.zosh.exception.UserException;

import java.util.List;
import java.util.Map;

/**
 * AI Chat Service — cung cấp chatbot AI cho hệ thống POS.
 * Hỗ trợ các loại câu hỏi:
 * - Tra cứu doanh thu, đơn hàng
 * - Phân tích chi nhánh, sản phẩm
 * - Cảnh báo tồn kho
 * - Tóm tắt dashboard
 */
public interface AiChatService {

    /**
     * Gửi câu hỏi cho AI và nhận câu trả lời dựa trên dữ liệu POS thực tế.
     *
     * @param message câu hỏi của người dùng
     * @param jwt     JWT token để xác thực
     * @return câu trả lời từ AI
     */
    String chat(String message, String jwt) throws UserException;

    /**
     * Lấy AI insight tóm tắt cho dashboard.
     *
     * @param jwt JWT token để xác thực
     * @return nhận xét tổng quan từ AI
     */
    String getDashboardInsight(String jwt) throws UserException;

    /**
     * Lấy danh sách gợi ý câu hỏi nhanh cho user.
     *
     * @return danh sách câu hỏi mẫu
     */
    List<String> getSuggestedQuestions();
}
