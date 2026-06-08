import React, { useState, useEffect, useRef, useCallback, useMemo } from "react";
import api from "@/utils/api";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { useSelector, useDispatch } from "react-redux";
import {
  selectCartItems,
  selectNote,
  selectPaymentMethod,
  selectSelectedCustomer,
  selectTotal,
  selectSubtotal,
  selectDiscountAmount,
  selectTax,
  setCurrentOrder,
  setPaymentMethod,
} from "../../../Redux Toolkit/features/cart/cartSlice";
import { useToast } from "../../../components/ui/use-toast";
import { createOrder } from "../../../Redux Toolkit/features/order/orderThunks";
import { paymentMethods } from "./data";
import {
  CheckCircle2,
  Loader2,
  ShoppingBag,
  User,
  Tag,
  FileText,
  Banknote,
  QrCode,
  Copy,
  CheckCheck,
} from "lucide-react";
import { Wifi, WifiOff } from "lucide-react";
import { fmtVND } from "@/utils/formatCurrency";

// ── Cấu hình tài khoản SePay VA ──────────────────────────────────
const BANK_CONFIG = {
  bankId: "MBBank",
  accountNo: "VQRQAJOHG9152",    // Số tài khoản VA do SePay cấp
  mainAccountNo: "9999999998628", // Tài khoản chính (để hiển thị)
  accountName: "HOANG NHU VIET",
};

const QUICK_AMOUNTS = [10000, 20000, 50000, 100000, 200000, 500000];

const PaymentDialog = ({
  showPaymentDialog,
  setShowPaymentDialog,
  setShowReceiptDialog,
}) => {
  const dispatch = useDispatch();
  const { toast } = useToast();
  const [processing, setProcessing] = useState(false);
  const [cashReceived, setCashReceived] = useState("");
  const [copied, setCopied] = useState(false);
  // QR Polling state
  const [qrPollingStatus, setQrPollingStatus] = useState("IDLE"); // IDLE | WAITING | PAID | ERROR
  const pollingIntervalRef = useRef(null);
  const cashInputRef = useRef(null);
  const qrOrderRef = useRef(`DH${Date.now().toString().slice(-7)}`);

  const paymentMethod = useSelector(selectPaymentMethod);
  const cart = useSelector(selectCartItems);
  const { branch } = useSelector((state) => state.branch);
  const { userProfile } = useSelector((state) => state.user);
  const selectedCustomer = useSelector(selectSelectedCustomer);
  const total = useSelector(selectTotal);
  const subtotal = useSelector(selectSubtotal);
  const discountAmount = useSelector(selectDiscountAmount);
  const tax = useSelector(selectTax);
  const note = useSelector(selectNote);

  const selectedMethod = paymentMethods.find((m) => m.key === paymentMethod);
  const cashAmount = parseFloat(cashReceived) || 0;
  const changeAmount = cashAmount - total;

  // SePay QR URL — amount phải là số nguyên VND (Math.round tránh lỗi thập phân)
  const sepayQRUrl = useMemo(() =>
    `https://qr.sepay.vn/img` +
    `?acc=${BANK_CONFIG.accountNo}` +
    `&bank=${BANK_CONFIG.bankId}` +
    `&amount=${Math.round(total)}` +
    `&des=${encodeURIComponent(qrOrderRef.current)}`,
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [total, qrOrderRef.current]
  );

  useEffect(() => {
    if (showPaymentDialog) {
      setCashReceived("");
      setCopied(false);
      setQrPollingStatus("IDLE");
      qrOrderRef.current = `DH${Date.now().toString().slice(-7)}`;
    } else {
      // Dừng polling khi đóng dialog
      stopPolling();
    }
  }, [showPaymentDialog]);

  // ── Khi chuyển sang UPI → đăng ký session + bắt đầu polling ──────
  useEffect(() => {
    if (paymentMethod === "UPI" && showPaymentDialog && total > 0) {
      startQrPolling();
    } else {
      stopPolling();
      if (paymentMethod !== "UPI") setQrPollingStatus("IDLE");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [paymentMethod, showPaymentDialog]);

  const stopPolling = () => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
  };

  const startQrPolling = async () => {
    stopPolling();
    const ref = qrOrderRef.current;
    setQrPollingStatus("WAITING");

    // 1. Đăng ký session với backend
    try {
      await api.post("/api/qr-payments/register", {
        orderRef: ref,
        amount: total,
      });
    } catch (err) {
      console.warn("QR session register failed (server có thể chưa restart):", err.message);
      // Vẫn cho polling tiếp để không block UX
    }

    // 2. Poll mỗi 3 giây
    pollingIntervalRef.current = setInterval(async () => {
      try {
        const res = await api.get(`/api/qr-payments/status/${ref}`);
        const status = res.data?.status;
        if (status === "PAID") {
          stopPolling();
          setQrPollingStatus("PAID");
          // Tự động tạo đơn hàng
          await processPayment(true);
        }
      } catch (err) {
        console.warn("QR status poll error:", err.message);
        setQrPollingStatus("ERROR");
      }
    }, 3000);
  };

  // Demo: Giả lập thanh toán thành công (bấm nút trong dialog)
  const simulatePayment = async () => {
    try {
      await api.post(`/api/webhook/simulate/${qrOrderRef.current}`);
      toast({ title: "🎭 Giả lập thành công", description: "Đang chờ hệ thống xác nhận..." });
    } catch (err) {
      toast({ title: "Lỗi simulate", description: err.message, variant: "destructive" });
    }
  };

  useEffect(() => {
    if (paymentMethod === "CASH") {
      setTimeout(() => cashInputRef.current?.focus(), 120);
    }
  }, [paymentMethod]);

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const processPayment = async (isAutoConfirm = false) => {
    // Validation chung — cả thủ công lẫn auto đều cần
    if (cart.length === 0) {
      toast({ title: "Giỏ hàng trống", description: "Vui lòng thêm sản phẩm trước khi thanh toán", variant: "destructive" });
      return;
    }
    if (!selectedCustomer) {
      if (isAutoConfirm) {
        // Auto-confirm nhưng chưa chọn khách → thông báo nhẹ nhàng, không block
        toast({ title: "⚠️ Đã nhận tiền", description: "Vui lòng chọn khách hàng rồi bấm xác nhận", variant: "default" });
        setQrPollingStatus("WAITING"); // Giữ trạng thái để cashier biết
        return;
      }
      toast({ title: "Chưa chọn khách hàng", description: "Vui lòng chọn khách hàng trước khi thanh toán", variant: "destructive" });
      return;
    }
    if (!branch) {
      toast({ title: "Lỗi chi nhánh", description: "Không tải được thông tin chi nhánh.", variant: "destructive" });
      return;
    }
    if (!isAutoConfirm && paymentMethod === "CASH" && cashAmount < total) {
      toast({ title: "Tiền chưa đủ", description: `Còn thiếu ${fmtVND(total - cashAmount)}`, variant: "destructive" });
      return;
    }

    setProcessing(true);
    try {
      const orderData = {
        totalAmount: total,
        discountAmount: discountAmount,
        branchId: branch.id,
        cashierId: userProfile.id,
        customer: selectedCustomer || null,
        items: cart.map((item) => ({
          productId: item.id,
          quantity: item.quantity,
          price: item.price,
          total: item.price * item.quantity,
        })),
        paymentType: paymentMethod,
        note: note || "",
      };
      const createdOrder = await dispatch(createOrder(orderData)).unwrap();
      dispatch(setCurrentOrder(createdOrder));

      // Cleanup session trên backend sau khi đơn hàng tạo thành công
      try {
        await api.delete(`/api/qr-payments/${qrOrderRef.current}`);
      } catch (_) { /* Không quan trọng nếu cleanup fail */ }

      stopPolling();
      setShowPaymentDialog(false);
      setShowReceiptDialog(true);
      toast({ title: "✅ Thanh toán thành công", description: `Đơn hàng #${createdOrder.id} đã được tạo` });
    } catch (error) {
      toast({ title: "Thanh toán thất bại", description: error || "Không thể tạo đơn hàng.", variant: "destructive" });
      // Nếu auto-confirm thất bại, cho phép cashier bấm thủ công
      if (isAutoConfirm) setQrPollingStatus("PAID");
    } finally {
      setProcessing(false);
    }
  };

  const handlePaymentMethod = (method) => {
    dispatch(setPaymentMethod(method));
    setCashReceived("");
  };

  const confirmLabel = {
    CASH: "Xác nhận & In biên lai",
    CARD: "Đã quẹt thẻ thành công",
    UPI: "Đã nhận tiền chuyển khoản",
  }[paymentMethod] ?? "Xác nhận thanh toán";

  // ─────────────────────────────────────────────────────────────────
  return (
    <Dialog open={showPaymentDialog} onOpenChange={setShowPaymentDialog}>
      {/*
        max-w-[900px]  → đủ rộng để 2 cột không bị ép
        overflow-hidden → bo góc sạch
        Không dùng overflow-y-auto ở đây → để nội dung bên trong tự quản lý scroll
      */}
      <DialogContent
        className="sm:!max-w-none p-0 gap-0 overflow-hidden rounded-2xl shadow-2xl"
        style={{ width: "min(98vw, 1060px)", maxWidth: "1060px" }}
      >

        {/* HEADER */}
        <DialogHeader className="px-6 py-4 bg-gradient-to-r from-primary/10 via-primary/5 to-transparent border-b shrink-0">
          <DialogTitle className="flex items-center gap-3 text-base font-semibold">
            <span className="w-8 h-8 rounded-lg bg-primary/15 flex items-center justify-center shrink-0">
              <ShoppingBag className="w-4 h-4 text-primary" />
            </span>
            Xác nhận thanh toán
            <Badge variant="outline" className="ml-auto text-xs font-normal shrink-0">
              {cart.length} sản phẩm
            </Badge>
          </DialogTitle>
        </DialogHeader>

        {/* BODY — flex row, chiều cao cố định để cả 2 cột đều fill và scroll được */}
        <div className="flex" style={{ height: "85vh" }}>

          {/* ══════════════ CỘT TRÁI ══════════════ */}
          <div className="flex-1 min-w-0 overflow-y-auto py-5 px-5 space-y-4">

            {/* Khách hàng */}
            {selectedCustomer && (
              <div className="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-primary/5 border border-primary/10">
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                  <User className="w-3.5 h-3.5 text-primary" />
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-semibold truncate">{selectedCustomer.fullName || selectedCustomer.name}</p>
                  <p className="text-xs text-muted-foreground">{selectedCustomer.phone}</p>
                </div>
              </div>
            )}

            {/* Sản phẩm */}
            <div>
              <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest mb-2">
                Sản phẩm ({cart.length})
              </p>
              <div className="space-y-1 max-h-44 overflow-y-auto pr-0.5">
                {cart.map((item) => (
                  <div key={item.id} className="flex items-center justify-between gap-3 px-2 py-1.5 rounded-lg hover:bg-muted/50 transition-colors">
                    <div className="flex items-center gap-2 min-w-0">
                      <span className="shrink-0 w-5 h-5 rounded-md bg-muted flex items-center justify-center text-[11px] font-bold text-muted-foreground">
                        {item.quantity}
                      </span>
                      <span className="text-sm truncate">{item.name}</span>
                    </div>
                    <span className="text-sm font-medium tabular-nums shrink-0">
                      {fmtVND((item.sellingPrice || item.price) * item.quantity)}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <Separator />

            {/* Tóm tắt tiền */}
            <div className="space-y-1.5 text-sm">
              <div className="flex justify-between text-muted-foreground">
                <span>Tạm tính</span>
                <span className="tabular-nums">{fmtVND(subtotal)}</span>
              </div>
              {discountAmount > 0 && (
                <div className="flex justify-between text-emerald-600 dark:text-emerald-400">
                  <span className="flex items-center gap-1"><Tag className="w-3 h-3" /> Giảm giá</span>
                  <span className="tabular-nums">− {fmtVND(discountAmount)}</span>
                </div>
              )}
              {tax > 0 && (
                <div className="flex justify-between text-muted-foreground">
                  <span>Thuế VAT</span>
                  <span className="tabular-nums">{fmtVND(tax)}</span>
                </div>
              )}
              <Separator />
              <div className="flex justify-between items-baseline pt-0.5">
                <span className="font-semibold">Tổng thanh toán</span>
                <span className="text-xl font-bold text-primary tabular-nums">{fmtVND(total)}</span>
              </div>
            </div>

            {/* Ghi chú */}
            {note && (
              <div className="flex gap-2 px-3 py-2 rounded-lg bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800">
                <FileText className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
                <span className="text-xs text-amber-800 dark:text-amber-300">{note}</span>
              </div>
            )}

            {/* ── CASH: Tiền thối ───────────────────────────────── */}
            {paymentMethod === "CASH" && (
              <div className="rounded-2xl border border-amber-200 dark:border-amber-800/70 overflow-hidden">
                <div className="flex items-center gap-2 px-4 py-2.5 bg-amber-50 dark:bg-amber-950/40 border-b border-amber-200 dark:border-amber-800/70">
                  <Banknote className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
                  <span className="text-xs font-semibold text-amber-700 dark:text-amber-300 uppercase tracking-wide">
                    Tính tiền thối
                  </span>
                </div>
                <div className="p-4 space-y-3 bg-white dark:bg-background">
                  {/* Input */}
                  <div className="flex items-center gap-3">
                    <label className="text-xs text-muted-foreground shrink-0 w-20">Khách đưa</label>
                    <input
                      ref={cashInputRef}
                      type="number"
                      min={0}
                      step={1000}
                      placeholder="0"
                      value={cashReceived}
                      onChange={(e) => setCashReceived(e.target.value)}
                      className="flex-1 h-9 px-3 text-sm font-semibold rounded-lg border border-input bg-background focus:outline-none focus:ring-2 focus:ring-primary/40 tabular-nums text-right"
                    />
                  </div>
                  {/* Mệnh giá nhanh */}
                  <div className="flex flex-wrap gap-1.5">
                    {QUICK_AMOUNTS.map((amt) => (
                      <button
                        key={amt}
                        type="button"
                        onClick={() => setCashReceived(String(amt >= total ? amt : Math.ceil(total / amt) * amt))}
                        className="text-[11px] px-2.5 py-1 rounded-lg border border-amber-300 dark:border-amber-700 bg-amber-50 dark:bg-amber-900/40 hover:bg-amber-100 dark:hover:bg-amber-800/60 text-amber-800 dark:text-amber-300 font-medium transition-all active:scale-95"
                      >
                        {fmtVND(amt)}
                      </button>
                    ))}
                  </div>
                  {/* Kết quả */}
                  {cashAmount > 0 && (
                    <div className={`flex items-center justify-between rounded-xl px-4 py-2.5 text-sm font-semibold border ${
                      changeAmount >= 0
                        ? "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800"
                        : "bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400 border-red-200 dark:border-red-800"
                    }`}>
                      <span className="text-xs">{changeAmount >= 0 ? "Tiền thối khách" : "Còn thiếu"}</span>
                      <span className="text-base tabular-nums font-bold">{fmtVND(Math.abs(changeAmount))}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* ── UPI: QR VietQR ────────────────────────────────── */}
            {paymentMethod === "UPI" && (
              <div className="rounded-2xl border border-sky-200 dark:border-sky-800/70 overflow-hidden">
                <div className="flex items-center gap-2 px-4 py-2.5 bg-sky-50 dark:bg-sky-950/40 border-b border-sky-200 dark:border-sky-800/70">
                  <QrCode className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
                  <span className="text-xs font-semibold text-sky-700 dark:text-sky-300 uppercase tracking-wide">
                    Quét QR để chuyển khoản
                  </span>
                </div>
                <div className="p-4 bg-white dark:bg-background space-y-3">
                  {/* Layout dọc: QR trên - info dưới */}
                  <div className="flex flex-col items-center gap-4">
                    {/* QR image từ SePay - canh giữa */}
                    <div className="relative w-[180px] h-[180px] rounded-xl border-2 border-sky-200 dark:border-sky-700 bg-white overflow-hidden shadow-md flex items-center justify-center">
                      <img
                        src={sepayQRUrl}
                        alt="QR chuyển khoản SePay"
                        className="w-full h-full object-contain"
                        onError={(e) => {
                          e.currentTarget.style.display = "none";
                          e.currentTarget.nextElementSibling.style.display = "flex";
                        }}
                      />
                      <div style={{ display: "none" }} className="w-full h-full items-center justify-center text-center p-3">
                        <span className="text-[10px] text-muted-foreground leading-relaxed">
                          Không tải được QR.<br />Kiểm tra internet.
                        </span>
                      </div>
                    </div>
                    {/* Badge SePay */}
                    <div className="flex items-center gap-1.5 text-[10px] text-muted-foreground -mt-2">
                      <span className="w-3.5 h-3.5 rounded-full bg-sky-500 flex items-center justify-center text-white font-bold" style={{fontSize:"7px"}}>S</span>
                      Powered by SePay × MBBank
                    </div>

                    {/* Thông tin ngân hàng - grid 2 cột */}
                    <div className="w-full grid grid-cols-2 gap-x-4 gap-y-2.5 text-xs">
                      <div>
                        <p className="text-muted-foreground mb-0.5">Ngân hàng</p>
                        <p className="font-semibold">MB Bank</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground mb-0.5">Chủ tài khoản</p>
                        <p className="font-semibold">{BANK_CONFIG.accountName}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground mb-0.5">Số TK địch (VA)</p>
                        <p className="font-mono font-bold tracking-wide text-sky-700 dark:text-sky-300">{BANK_CONFIG.accountNo}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground mb-0.5">Số tiền</p>
                        <p className="font-bold text-primary tabular-nums">{fmtVND(total)}</p>
                      </div>
                      <div className="col-span-2 pt-1 border-t border-sky-100 dark:border-sky-800">
                        <p className="text-muted-foreground mb-1">Nội dung chuyển khoản</p>
                        <p className="font-mono font-bold text-sky-700 dark:text-sky-300 tracking-widest text-sm">
                          {qrOrderRef.current}
                        </p>
                        <p className="text-[10px] text-muted-foreground mt-0.5">
                          ⚠️ Nhập đúng nội dung này để hệ thống tự xác nhận
                        </p>
                      </div>
                    </div>
                  </div>
                  {/* Nút copy nội dung CK */}
                  <button
                    onClick={() => handleCopy(qrOrderRef.current)}
                    className="w-full flex items-center justify-center gap-2 py-2 rounded-lg border border-sky-300 dark:border-sky-700 bg-sky-50 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300 text-xs font-medium hover:bg-sky-100 dark:hover:bg-sky-800/40 transition-all active:scale-[0.98]"
                  >
                    {copied ? <><CheckCheck className="w-3.5 h-3.5 text-emerald-500" /> Đã sao chép!</> : <><Copy className="w-3.5 h-3.5" /> Sao chép nội dung chuyển khoản</>}
                  </button>

                  {/* ── Trạng thái polling SePay ── */}
                  {qrPollingStatus === "WAITING" && (
                    <div className="flex items-center justify-between gap-3 px-3 py-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800">
                      <div className="flex items-center gap-2">
                        <span className="relative flex h-2.5 w-2.5">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                        </span>
                        <span className="text-xs text-emerald-700 dark:text-emerald-300 font-medium">
                          Đang chờ chuyển khoản...
                        </span>
                      </div>
                      <Wifi className="w-3.5 h-3.5 text-emerald-500 animate-pulse" />
                    </div>
                  )}

                  {qrPollingStatus === "PAID" && (
                    <div className="flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-emerald-100 dark:bg-emerald-900/40 border border-emerald-300 dark:border-emerald-700">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      <span className="text-sm font-semibold text-emerald-700 dark:text-emerald-300">
                        Đã nhận tiền — Đang tạo đơn...
                      </span>
                    </div>
                  )}

                  {qrPollingStatus === "ERROR" && (
                    <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-orange-50 dark:bg-orange-950/30 border border-orange-200 dark:border-orange-800">
                      <WifiOff className="w-3.5 h-3.5 text-orange-500" />
                      <span className="text-xs text-orange-700 dark:text-orange-300">
                        Mất kết nối polling. Backend có thể chưa khởi động.
                      </span>
                    </div>
                  )}

                  {/* Nút Demo: giả lập thanh toán */}
                  <button
                    onClick={simulatePayment}
                    className="w-full flex items-center justify-center gap-2 py-1.5 rounded-lg border border-dashed border-violet-300 dark:border-violet-700 text-violet-600 dark:text-violet-400 text-[11px] font-medium hover:bg-violet-50 dark:hover:bg-violet-950/30 transition-all"
                    title="Chỉ dùng để demo — giả lập SePay gọi webhook"
                  >
                    🎭 [DEMO] Giả lập nhận tiền thành công
                  </button>
                </div>
              </div>
            )}

          </div>{/* end cột trái */}

          {/* ══════════════ CỘT PHẢI ══════════════ */}
          <div className="w-[280px] shrink-0 border-l flex flex-col bg-muted/10">

            {/* Phương thức */}
            <div className="p-4 flex-1 overflow-y-auto min-h-0">
              <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest mb-3">
                Phương thức
              </p>
              <div className="space-y-2">
                {paymentMethods.map((method) => {
                  const isSelected = paymentMethod === method.key;
                  return (
                    <button
                      key={method.key}
                      onClick={() => handlePaymentMethod(method.key)}
                      className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl border-2 text-left transition-all duration-150 active:scale-[0.98] ${
                        isSelected
                          ? "border-primary bg-primary/8 shadow-sm"
                          : "border-border/60 bg-card hover:border-primary/30 hover:bg-muted/50"
                      }`}
                    >
                      <span className="text-lg leading-none">{method.icon}</span>
                      <div className="flex-1 min-w-0">
                        <p className={`text-[13px] font-semibold leading-none mb-0.5 ${isSelected ? "text-primary" : "text-foreground"}`}>
                          {method.label}
                        </p>
                        <p className="text-[11px] text-muted-foreground line-clamp-1">{method.description}</p>
                      </div>
                      {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-primary shrink-0" />}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Tổng + nút xác nhận (sticky bottom) */}
            <div className="p-4 border-t bg-card space-y-3 shrink-0">
              {/* Card tổng */}
              <div className="rounded-xl bg-primary/5 border border-primary/15 px-3 py-3 text-center">
                <p className="text-[11px] text-muted-foreground mb-0.5">Cần thu</p>
                <p className="text-[22px] font-bold text-primary tabular-nums leading-tight">{fmtVND(total)}</p>
                {selectedMethod && (
                  <p className="text-[11px] text-muted-foreground mt-0.5">
                    {selectedMethod.icon} {selectedMethod.label}
                  </p>
                )}
                {paymentMethod === "CASH" && cashAmount > 0 && changeAmount >= 0 && (
                  <div className="mt-2 text-xs font-semibold text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg py-1.5 border border-emerald-200 dark:border-emerald-800">
                    Thối: {fmtVND(changeAmount)}
                  </div>
                )}
              </div>

              {/* Xác nhận */}
              <Button
                className="w-full h-11 text-sm font-semibold gap-2 shadow-sm"
                onClick={processPayment}
                disabled={processing}
              >
                {processing ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Đang xử lý...</>
                ) : (
                  <><CheckCircle2 className="w-4 h-4 shrink-0" /><span className="truncate">{confirmLabel}</span></>
                )}
              </Button>

              <Button
                variant="ghost"
                size="sm"
                className="w-full text-muted-foreground hover:text-foreground"
                onClick={() => setShowPaymentDialog(false)}
                disabled={processing}
              >
                Hủy
              </Button>
            </div>

          </div>{/* end cột phải */}

        </div>{/* end body */}
      </DialogContent>
    </Dialog>
  );
};

export default PaymentDialog;
