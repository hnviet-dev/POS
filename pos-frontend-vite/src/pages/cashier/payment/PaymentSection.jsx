import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { useToast } from "../../../components/ui/use-toast";
import {
  holdOrder,
  selectCartItems,
  selectSelectedCustomer,
  selectTotal,
} from "../../../Redux Toolkit/features/cart/cartSlice";
import { Button } from "../../../components/ui/button";
import { CreditCard, Pause, AlertCircle } from "lucide-react";

const PaymentSection = ({ setShowPaymentDialog }) => {
  const cartItems = useSelector(selectCartItems);
  const selectedCustomer = useSelector(selectSelectedCustomer);
  const total = useSelector(selectTotal);
  const { toast } = useToast();
  const dispatch = useDispatch();

  // ── Logic giữ nguyên ───────────────────────────────────────────────
  const handlePayment = () => {
    if (cartItems.length === 0) {
      toast({ title: "Giỏ hàng trống", description: "Vui lòng thêm sản phẩm vào giỏ hàng", variant: "destructive" });
      return;
    }
    if (!selectedCustomer) {
      toast({ title: "Chưa chọn khách hàng", description: "Vui lòng chọn khách hàng trước khi thanh toán", variant: "destructive" });
      return;
    }
    setShowPaymentDialog(true);
  };

  const handleHoldOrder = () => {
    if (cartItems.length === 0) {
      toast({ title: "Giỏ hàng trống", description: "Không có sản phẩm nào để giữ đơn", variant: "destructive" });
      return;
    }
    dispatch(holdOrder());
    toast({ title: "Đã giữ đơn hàng", description: "Đơn hàng được tạm giữ, có thể tiếp tục sau" });
  };
  // ──────────────────────────────────────────────────────────────────

  const isEmpty = cartItems.length === 0;
  const missingCustomer = !isEmpty && !selectedCustomer;

  return (
    <div className="mt-auto p-4 flex flex-col gap-3">
      {/* Tổng tiền */}
      <div className="rounded-xl bg-primary/5 border border-primary/10 p-3 text-center">
        <p className="text-xs text-muted-foreground mb-0.5">Tổng thanh toán</p>
        <p className="text-2xl font-bold text-primary tabular-nums">
          {total.toLocaleString("vi-VN")}₫
        </p>
      </div>

      {/* Cảnh báo thiếu khách hàng */}
      {missingCustomer && (
        <div className="flex items-center gap-2 text-xs text-amber-600 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 rounded-lg px-3 py-2">
          <AlertCircle className="w-3.5 h-3.5 flex-shrink-0" />
          Chưa chọn khách hàng
        </div>
      )}

      {/* Nút thanh toán chính */}
      <Button
        className="w-full h-11 text-base font-semibold"
        onClick={handlePayment}
        disabled={isEmpty}
      >
        <CreditCard className="w-4 h-4 mr-2" />
        Thanh toán
      </Button>

      {/* Giữ đơn */}
      <Button
        variant="outline"
        className="w-full h-9 text-sm"
        onClick={handleHoldOrder}
        disabled={isEmpty}
      >
        <Pause className="w-4 h-4 mr-2" />
        Giữ đơn
      </Button>
    </div>
  );
};

export default PaymentSection;
