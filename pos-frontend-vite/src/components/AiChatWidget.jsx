import React, { useState, useRef, useEffect, useCallback } from "react";
import api from "@/utils/api";
import {
  MessageCircle,
  X,
  Send,
  Bot,
  User,
  Sparkles,
  Loader2,
  Trash2,
  Lightbulb,
  Minimize2,
  ChevronUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";

// ────────────────────────────────────────────
// AI CHATBOT WIDGET — Floating chat cho POS
// Redesigned to match the system's design language
// ────────────────────────────────────────────

const AiChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Auto scroll to bottom
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Load suggestions on first open
  useEffect(() => {
    if (isOpen && suggestions.length === 0) {
      loadSuggestions();
    }
  }, [isOpen]);

  // Add welcome message on first open
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([
        {
          role: "ai",
          content:
            "Xin chào! 👋 Tôi là **POS AI Assistant**.\n\nTôi có thể giúp bạn:\n- 📊 Tra cứu doanh thu, đơn hàng\n- 📦 Kiểm tra tồn kho\n- 📈 Phân tích xu hướng bán hàng\n- 🏪 So sánh chi nhánh\n\nHãy hỏi tôi bất cứ điều gì!",
          timestamp: new Date(),
        },
      ]);
    }
  }, [isOpen]);

  const loadSuggestions = async () => {
    try {
      const jwt = localStorage.getItem("jwt");
      const res = await api.get("/api/ai/suggestions", {
        headers: { Authorization: `Bearer ${jwt}` },
      });
      setSuggestions(res.data.suggestions || []);
    } catch (err) {
      // Use default suggestions if API fails
      setSuggestions([
        "Doanh thu hôm nay bao nhiêu?",
        "Sản phẩm nào bán chạy nhất?",
        "Có sản phẩm nào sắp hết hàng không?",
        "So sánh doanh thu hôm nay với hôm qua",
      ]);
    }
  };

  const sendMessage = async (text) => {
    const messageText = text || input.trim();
    if (!messageText || loading) return;

    const userMsg = {
      role: "user",
      content: messageText,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    setShowSuggestions(false);

    try {
      const jwt = localStorage.getItem("jwt");
      const res = await api.post(
        "/api/ai/chat",
        { message: messageText },
        { headers: { Authorization: `Bearer ${jwt}` } }
      );

      const aiMsg = {
        role: "ai",
        content: res.data.reply || "Không nhận được phản hồi.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      const errorMsg = {
        role: "ai",
        content:
          "⚠️ Lỗi kết nối. Vui lòng kiểm tra:\n- Backend đang chạy?\n- Gemini API key đã cấu hình?",
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: "ai",
        content: "Đã xóa lịch sử chat. Hãy hỏi tôi bất cứ điều gì! 🤖",
        timestamp: new Date(),
      },
    ]);
    setShowSuggestions(true);
  };

  const getDashboardInsight = async () => {
    setLoading(true);
    try {
      const jwt = localStorage.getItem("jwt");
      const res = await api.get("/api/ai/dashboard-insight", {
        headers: { Authorization: `Bearer ${jwt}` },
      });

      const aiMsg = {
        role: "ai",
        content: res.data.insight || "Không có dữ liệu phân tích.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "⚠️ Không thể tải phân tích dashboard.",
          timestamp: new Date(),
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Format AI message content (basic markdown)
  const formatContent = (content) => {
    if (!content) return "";

    return content
      .split("\n")
      .map((line, i) => {
        // Bold
        let formatted = line.replace(
          /\*\*(.*?)\*\*/g,
          '<strong class="font-semibold text-foreground">$1</strong>'
        );
        // Code
        formatted = formatted.replace(
          /`([^`]+)`/g,
          '<code class="bg-muted text-foreground px-1.5 py-0.5 rounded text-xs font-mono">$1</code>'
        );
        // Bullet points
        if (formatted.startsWith("- ")) {
          formatted = `<span class="flex gap-1.5 items-start"><span class="text-primary mt-0.5 shrink-0">•</span><span>${formatted.slice(2)}</span></span>`;
        }
        // Numbered list
        const numMatch = formatted.match(/^(\d+)\.\s/);
        if (numMatch) {
          formatted = `<span class="flex gap-1.5 items-start"><span class="font-semibold text-primary shrink-0">${numMatch[1]}.</span><span>${formatted.slice(numMatch[0].length)}</span></span>`;
        }

        return formatted;
      })
      .join("<br/>");
  };

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <>
      {/* ═══ FLOATING BUTTON ═══ */}
      {!isOpen && (
        <Tooltip>
          <TooltipTrigger asChild>
            <button
              id="ai-chat-toggle"
              onClick={() => setIsOpen(true)}
              className={cn(
                "fixed bottom-6 right-6 z-[9999]",
                "w-14 h-14 rounded-full",
                "bg-primary text-primary-foreground",
                "flex items-center justify-center",
                "shadow-lg hover:shadow-xl",
                "transition-all duration-300 ease-out",
                "hover:scale-110 active:scale-95",
                "animate-[ai-fab-pulse_2.5s_ease-in-out_infinite]",
                "cursor-pointer border-0"
              )}
            >
              <Bot size={26} />
            </button>
          </TooltipTrigger>
          <TooltipContent side="left">
            <p>AI Assistant</p>
          </TooltipContent>
        </Tooltip>
      )}

      {/* ═══ CHAT WINDOW ═══ */}
      {isOpen && (
        <div
          className={cn(
            "fixed bottom-6 right-6 z-[9999]",
            "w-[400px] h-[580px]",
            "rounded-2xl overflow-hidden",
            "flex flex-col",
            "bg-card border border-border",
            "shadow-2xl",
            "animate-[ai-chat-slide-up_0.35s_ease-out]",
            "font-sans"
          )}
        >
          {/* ─── HEADER ─── */}
          <div
            className={cn(
              "bg-primary text-primary-foreground",
              "px-5 py-4",
              "flex items-center justify-between",
              "shrink-0"
            )}
          >
            <div className="flex items-center gap-3">
              <Avatar className="h-9 w-9 rounded-xl bg-primary-foreground/15">
                <AvatarFallback className="rounded-xl bg-transparent text-primary-foreground">
                  <Sparkles size={20} />
                </AvatarFallback>
              </Avatar>
              <div>
                <div className="font-bold text-[15px] leading-tight">
                  POS AI Assistant
                </div>
                <div className="text-primary-foreground/60 text-[11px] mt-0.5 flex items-center gap-1.5">
                  <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Powered by Gemini AI
                </div>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <Tooltip>
                <TooltipTrigger asChild>
                  <button
                    id="ai-insight-btn"
                    onClick={getDashboardInsight}
                    disabled={loading}
                    className={cn(
                      "inline-flex items-center gap-1.5",
                      "bg-primary-foreground/15 hover:bg-primary-foreground/25",
                      "text-primary-foreground text-[11px] font-medium",
                      "rounded-lg px-2.5 py-1.5",
                      "transition-colors duration-200",
                      "border-0 cursor-pointer",
                      "disabled:opacity-50 disabled:cursor-not-allowed"
                    )}
                  >
                    <Sparkles size={13} />
                    Insight
                  </button>
                </TooltipTrigger>
                <TooltipContent side="bottom">
                  <p>Phân tích tổng quan Dashboard</p>
                </TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <button
                    id="ai-clear-btn"
                    onClick={clearChat}
                    className={cn(
                      "bg-primary-foreground/15 hover:bg-primary-foreground/25",
                      "text-primary-foreground",
                      "rounded-lg p-1.5",
                      "transition-colors duration-200",
                      "border-0 cursor-pointer"
                    )}
                  >
                    <Trash2 size={15} />
                  </button>
                </TooltipTrigger>
                <TooltipContent side="bottom">
                  <p>Xóa lịch sử</p>
                </TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <button
                    id="ai-close-btn"
                    onClick={() => setIsOpen(false)}
                    className={cn(
                      "bg-primary-foreground/15 hover:bg-primary-foreground/25",
                      "text-primary-foreground",
                      "rounded-lg p-1.5",
                      "transition-colors duration-200",
                      "border-0 cursor-pointer"
                    )}
                  >
                    <X size={15} />
                  </button>
                </TooltipTrigger>
                <TooltipContent side="bottom">
                  <p>Đóng</p>
                </TooltipContent>
              </Tooltip>
            </div>
          </div>

          {/* ─── MESSAGES ─── */}
          <ScrollArea className="flex-1 min-h-0 overflow-hidden">
            <div
              ref={chatContainerRef}
              className="p-4 flex flex-col gap-4"
            >
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={cn(
                    "flex gap-2.5 animate-[ai-msg-fade-in_0.3s_ease-out]",
                    msg.role === "user" ? "justify-end" : "justify-start"
                  )}
                >
                  {/* AI Avatar */}
                  {msg.role === "ai" && (
                    <Avatar
                      className={cn(
                        "h-7 w-7 shrink-0 mt-0.5 rounded-lg",
                        msg.isError
                          ? "bg-destructive/15"
                          : "bg-primary/10"
                      )}
                    >
                      <AvatarFallback
                        className={cn(
                          "rounded-lg bg-transparent",
                          msg.isError
                            ? "text-destructive"
                            : "text-primary"
                        )}
                      >
                        <Bot size={15} />
                      </AvatarFallback>
                    </Avatar>
                  )}

                  {/* Message bubble */}
                  <div className="flex flex-col gap-1 max-w-[80%]">
                    <div
                      className={cn(
                        "px-3.5 py-2.5 text-[13px] leading-relaxed",
                        msg.role === "user"
                          ? "bg-primary text-primary-foreground rounded-2xl rounded-br-md"
                          : msg.isError
                            ? "bg-destructive/10 text-destructive border border-destructive/20 rounded-2xl rounded-bl-md"
                            : "bg-muted text-foreground border border-border rounded-2xl rounded-bl-md"
                      )}
                      dangerouslySetInnerHTML={{
                        __html: formatContent(msg.content),
                      }}
                    />
                    <span
                      className={cn(
                        "text-[10px] text-muted-foreground px-1",
                        msg.role === "user" ? "text-right" : "text-left"
                      )}
                    >
                      {formatTime(msg.timestamp)}
                    </span>
                  </div>

                  {/* User Avatar */}
                  {msg.role === "user" && (
                    <Avatar className="h-7 w-7 shrink-0 mt-0.5 rounded-lg bg-primary/20">
                      <AvatarFallback className="rounded-lg bg-transparent text-primary">
                        <User size={15} />
                      </AvatarFallback>
                    </Avatar>
                  )}
                </div>
              ))}

              {/* Loading indicator */}
              {loading && (
                <div className="flex gap-2.5 animate-[ai-msg-fade-in_0.3s_ease-out]">
                  <Avatar className="h-7 w-7 shrink-0 mt-0.5 rounded-lg bg-primary/10">
                    <AvatarFallback className="rounded-lg bg-transparent text-primary">
                      <Loader2 size={15} className="animate-spin" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="bg-muted border border-border rounded-2xl rounded-bl-md px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-[ai-dot-bounce_1.4s_ease-in-out_infinite]" />
                        <span className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-[ai-dot-bounce_1.4s_ease-in-out_0.2s_infinite]" />
                        <span className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-[ai-dot-bounce_1.4s_ease-in-out_0.4s_infinite]" />
                      </div>
                      <span className="text-muted-foreground text-[12px]">
                        Đang phân tích...
                      </span>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* ─── SUGGESTIONS ─── */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="border-t border-border bg-card px-4 py-2.5">
              <div className="flex items-center gap-1.5 mb-2">
                <Lightbulb size={12} className="text-yellow-500" />
                <span className="text-[11px] text-muted-foreground font-medium">
                  Gợi ý câu hỏi
                </span>
              </div>
              <div className="flex gap-1.5 flex-wrap">
                {suggestions.slice(0, 4).map((s, i) => (
                  <button
                    key={i}
                    id={`ai-suggestion-${i}`}
                    onClick={() => sendMessage(s)}
                    className={cn(
                      "text-[11px] px-2.5 py-1 rounded-full",
                      "bg-muted text-muted-foreground",
                      "border border-border",
                      "hover:bg-accent hover:text-accent-foreground hover:border-primary/30",
                      "transition-all duration-200",
                      "cursor-pointer whitespace-nowrap"
                    )}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* ─── INPUT ─── */}
          <div className="border-t border-border bg-card p-3 shrink-0">
            <div className="flex gap-2 items-center">
              <input
                ref={inputRef}
                id="ai-chat-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Hỏi gì đó... (VD: doanh thu hôm nay?)"
                disabled={loading}
                className={cn(
                  "flex-1 h-10 px-3.5 rounded-xl text-sm",
                  "bg-muted/50 text-foreground",
                  "border border-border",
                  "placeholder:text-muted-foreground",
                  "focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50",
                  "transition-all duration-200",
                  "disabled:opacity-50 disabled:cursor-not-allowed"
                )}
              />
              <Tooltip>
                <TooltipTrigger asChild>
                  <button
                    id="ai-send-btn"
                    onClick={() => sendMessage()}
                    disabled={!input.trim() || loading}
                    className={cn(
                      "w-10 h-10 rounded-xl",
                      "flex items-center justify-center",
                      "border-0 shrink-0",
                      "transition-all duration-200 cursor-pointer",
                      input.trim() && !loading
                        ? "bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm"
                        : "bg-muted text-muted-foreground cursor-not-allowed"
                    )}
                  >
                    <Send size={17} />
                  </button>
                </TooltipTrigger>
                <TooltipContent side="top">
                  <p>Gửi tin nhắn</p>
                </TooltipContent>
              </Tooltip>
            </div>
          </div>
        </div>
      )}

      {/* ═══ ANIMATIONS ═══ */}
      <style>{`
        @keyframes ai-fab-pulse {
          0%, 100% { box-shadow: 0 4px 20px oklch(var(--primary) / 0.3); }
          50% { box-shadow: 0 4px 32px oklch(var(--primary) / 0.5); }
        }
        @keyframes ai-chat-slide-up {
          from { opacity: 0; transform: translateY(16px) scale(0.97); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes ai-msg-fade-in {
          from { opacity: 0; transform: translateY(6px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes ai-dot-bounce {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
          40% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </>
  );
};

export default AiChatWidget;
