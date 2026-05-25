package com.zosh.controller;

import com.zosh.exception.UserException;
import com.zosh.service.AiChatService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * AI Chatbot Controller — API endpoints cho chatbot AI trong hệ thống POS.
 *
 * Endpoints:
 * POST /api/ai/chat — Gửi câu hỏi cho AI
 * GET /api/ai/dashboard-insight — Lấy AI insight cho dashboard
 * GET /api/ai/suggestions — Lấy danh sách câu hỏi gợi ý
 */
@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiChatController {

    private final AiChatService aiChatService;

    /**
     * Gửi tin nhắn cho AI chatbot.
     * Request body: { "message": "Doanh thu hôm nay?" }
     * Response: { "reply": "...", "timestamp": "..." }
     */
    @PostMapping("/chat")
    public ResponseEntity<Map<String, Object>> chat(
            @RequestBody Map<String, String> request,
            @RequestHeader("Authorization") String jwt) throws UserException {

        String message = request.get("message");

        if (message == null || message.trim().isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "Message is required",
                    "timestamp", System.currentTimeMillis()));
        }

        String reply = aiChatService.chat(message.trim(), jwt);

        return ResponseEntity.ok(Map.of(
                "reply", reply,
                "timestamp", System.currentTimeMillis()));
    }

    /**
     * Lấy AI insight tóm tắt cho dashboard.
     * Response: { "insight": "📊 Doanh thu hôm nay tăng 15%...", "timestamp": "..."
     * }
     */
    @GetMapping("/dashboard-insight")
    public ResponseEntity<Map<String, Object>> getDashboardInsight(
            @RequestHeader("Authorization") String jwt) throws UserException {

        String insight = aiChatService.getDashboardInsight(jwt);

        return ResponseEntity.ok(Map.of(
                "insight", insight,
                "timestamp", System.currentTimeMillis()));
    }

    /**
     * Lấy danh sách câu hỏi gợi ý nhanh cho chatbot.
     * Response: { "suggestions": ["Doanh thu hôm nay?", ...] }
     */
    @GetMapping("/suggestions")
    public ResponseEntity<Map<String, Object>> getSuggestions() {
        List<String> suggestions = aiChatService.getSuggestedQuestions();

        return ResponseEntity.ok(Map.of(
                "suggestions", suggestions));
    }
}
