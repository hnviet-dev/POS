import React from "react";
import { Separator } from "../../../components/ui/separator";
import { useSelector } from "react-redux";
import {
  selectDiscountAmount,
  selectSubtotal,
  selectTax,
  selectTotal,
} from "../../../Redux Toolkit/features/cart/cartSlice";
import { fmtVND } from "@/utils/formatCurrency";

const CartSummary = () => {
  const subtotal = useSelector(selectSubtotal);
  const tax = useSelector(selectTax);
  const discountAmount = useSelector(selectDiscountAmount);
  const total = useSelector(selectTotal);

  return (
    <div className="border-t bg-muted/50 px-4 py-3">
      <div className="space-y-1.5 text-sm">
        <div className="flex justify-between text-muted-foreground">
          <span>Tạm tính</span>
          <span>{fmtVND(subtotal)}</span>
        </div>

        {tax > 0 && (
          <div className="flex justify-between text-muted-foreground">
            <span>Thuế</span>
            <span>{fmtVND(tax)}</span>
          </div>
        )}

        {discountAmount > 0 && (
          <div className="flex justify-between text-emerald-600">
            <span>Giảm giá</span>
            <span>- {fmtVND(discountAmount)}</span>
          </div>
        )}

        <Separator className="my-1" />

        <div className="flex justify-between font-bold text-base">
          <span>Tổng cộng</span>
          <span className="text-primary">{fmtVND(total)}</span>
        </div>
      </div>
    </div>
  );
};

export default CartSummary;
