import React, { useState } from "react";
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
  ChevronRight,
} from "lucide-react";

const fmtVND = (amount) =>
  (amount || 0).toLocaleString("vi-VN") + "₫";

const PaymentDialog = ({
  showPaymentDialog,
  setShowPaymentDialog,
  setShowReceiptDialog,
}) => {
  const dispatch = useDispatch();
  const { toast } = useToast();
  const [processing, setProcessing] = useState(false);

  // ── Selectors (logic giữ nguyên) ──────────────────────────────────
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

  // ── processPayment — logic giữ nguyên, chỉ thêm loading state ─────
  const processPayment = async () => {
    if (cart.length === 0) {
      toast({ title: "Giỏ hàng trống", description: "Vui lòng thêm sản phẩm trước khi thanh toán", variant: "destructive" });
      return;
    }
    if (!selectedCustomer) {
      toast({ title: "Chưa chọn khách hàng", description: "Vui lòng chọn khách hàng trước khi thanh toán", variant: "destructive" });
      return;
    }
    if (!branch) {
      toast({ title: "Lỗi chi nhánh", description: "Không tải được thông tin chi nhánh. Vui lòng thử lại.", variant: "destructive" });
      return;
    }

    setProcessing(true);
    try {
      const orderData = {
        totalAmount: total,
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

      setShowPaymentDialog(false);
      setShowReceiptDialog(true);

      toast({
        title: "Thanh toán thành công",
        description: `Đơn hàng #${createdOrder.id} đã được tạo`,
      });
    } catch (error) {
      toast({
        title: "Thanh toán thất bại",
        description: error || "Không thể tạo đơn hàng. Vui lòng thử lại.",
        variant: "destructive",
      });
    } finally {
      setProcessing(false);
    }
  };

  const handlePaymentMethod = (method) => dispatch(setPaymentMethod(method));

  // ── Render ─────────────────────────────────────────────────────────
  return (
    <Dialog open={showPaymentDialog} onOpenChange={setShowPaymentDialog}>
      <DialogContent className="max-w-2xl p-0 gap-0 overflow-hidden">
        {/* Header */}
        <DialogHeader className="px-6 pt-5 pb-4 border-b bg-muted/40">
          <DialogTitle className="flex items-center gap-2 text-lg">
            <ShoppingBag className="w-5 h-5 text-primary" />
            Xác nhận thanh toán
          </DialogTitle>
        </DialogHeader>

        <div className="flex divide-x">
          {/* ─── Cột trái: Tóm tắt đơn hàng ─────────────────────── */}
          <div className="flex-1 flex flex-col p-5 gap-4">
            {/* Thông tin khách */}
            {selectedCustomer && (
              <div className="flex items-center gap-3 p-3 rounded-lg bg-primary/5 border border-primary/10">
                <div className="w-9 h-9 rounded-full bg-primary/15 flex items-center justify-center flex-shrink-0">
                  <User className="w-4 h-4 text-primary" />
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-semibold truncate">
                    {selectedCustomer.fullName || selectedCustomer.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {selectedCustomer.phone}
                  </p>
                </div>
              </div>
            )}

            {/* Danh sách sản phẩm */}
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
                Sản phẩm ({cart.length})
              </p>
              <div className="space-y-2 max-h-44 overflow-y-auto pr-1">
                {cart.map((item) => (
                  <div key={item.id} className="flex items-center justify-between gap-2 text-sm">
                    <div className="flex items-center gap-2 min-w-0">
                      <Badge variant="secondary" className="text-xs px-1.5 py-0 flex-shrink-0">
                        ×{item.quantity}
                      </Badge>
                      <span className="truncate text-foreground">{item.name}</span>
                    </div>
                    <span className="font-medium flex-shrink-0 text-foreground">
                      {fmtVND((item.sellingPrice || item.price) * item.quantity)}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <Separator />

            {/* Breakdown */}
            <div className="space-y-2 text-sm">
              <div className="flex justify-between text-muted-foreground">
                <span>Tạm tính</span>
                <span>{fmtVND(subtotal)}</span>
              </div>
              {discountAmount > 0 && (
                <div className="flex justify-between text-emerald-600">
                  <span className="flex items-center gap-1">
                    <Tag className="w-3 h-3" /> Giảm giá
                  </span>
                  <span>- {fmtVND(discountAmount)}</span>
                </div>
              )}
              {tax > 0 && (
                <div className="flex justify-between text-muted-foreground">
                  <span>Thuế</span>
                  <span>{fmtVND(tax)}</span>
                </div>
              )}
              <Separator />
              <div className="flex justify-between text-base font-bold">
                <span>Tổng cộng</span>
                <span className="text-primary text-lg">{fmtVND(total)}</span>
              </div>
            </div>

            {/* Ghi chú */}
            {note && (
              <div className="flex gap-2 p-2.5 rounded-md bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 text-sm">
                <FileText className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
                <span className="text-amber-800 dark:text-amber-300 text-xs">{note}</span>
              </div>
            )}
          </div>

          {/* ─── Cột phải: Chọn phương thức thanh toán ───────────── */}
          <div className="w-60 flex flex-col p-5 gap-4 bg-muted/20">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
              Phương thức thanh toán
            </p>

            <div className="space-y-2">
              {paymentMethods.map((method) => {
                const isSelected = paymentMethod === method.key;
                return (
                  <button
                    key={method.key}
                    onClick={() => handlePaymentMethod(method.key)}
                    className={`w-full flex items-center gap-3 p-3 rounded-xl border-2 text-left transition-all duration-150 ${
                      isSelected
                        ? "border-primary bg-primary/8 shadow-sm"
                        : "border-border bg-card hover:border-primary/40 hover:bg-muted/60"
                    }`}
                  >
                    <span className="text-xl leading-none">{method.icon}</span>
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-semibold leading-none mb-0.5 ${isSelected ? "text-primary" : "text-foreground"}`}>
                        {method.label}
                      </p>
                      <p className="text-xs text-muted-foreground truncate">
                        {method.description}
                      </p>
                    </div>
                    {isSelected && (
                      <CheckCircle2 className="w-4 h-4 text-primary flex-shrink-0" />
                    )}
                  </button>
                );
              })}
            </div>

            {/* Tổng ở cột phải để confirm dễ */}
            <div className="mt-auto pt-4 border-t space-y-3">
              <div className="text-center">
                <p className="text-xs text-muted-foreground mb-1">Số tiền cần thu</p>
                <p className="text-2xl font-bold text-primary tabular-nums">
                  {fmtVND(total)}
                </p>
                {selectedMethod && (
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {selectedMethod.icon} {selectedMethod.label}
                  </p>
                )}
              </div>

              <Button
                className="w-full h-11 text-base font-semibold"
                onClick={processPayment}
                disabled={processing}
              >
                {processing ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Đang xử lý...
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="w-4 h-4 mr-2" />
                    Xác nhận thanh toán
                  </>
                )}
              </Button>

              <Button
                variant="ghost"
                className="w-full h-9 text-sm"
                onClick={() => setShowPaymentDialog(false)}
                disabled={processing}
              >
                Hủy
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default PaymentDialog;
