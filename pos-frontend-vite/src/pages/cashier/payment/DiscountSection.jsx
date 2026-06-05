import React from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  selectDiscount,
  selectDiscountAmount,
  selectSubtotal,
  setDiscount,
} from "../../../Redux Toolkit/features/cart/cartSlice";
import { Tag } from "lucide-react";
import { Input } from "@/components/ui/input";
import { fmtVND } from "@/utils/formatCurrency";

const DiscountSection = () => {
  const dispatch = useDispatch();
  const discount = useSelector(selectDiscount);
  const discountAmount = useSelector(selectDiscountAmount);
  const subtotal = useSelector(selectSubtotal);

  const handleSetValue = (e) => {
    const raw = parseFloat(e.target.value) || 0;
    // Giới hạn: % không quá 100, fixed không quá subtotal
    const capped =
      discount.type === "percentage"
        ? Math.min(raw, 100)
        : Math.min(raw, subtotal);
    dispatch(setDiscount({ ...discount, value: capped }));
  };

  const handleSetType = (type) => {
    // Fix bug cũ: phải dispatch, không gọi thẳng action creator
    dispatch(setDiscount({ ...discount, type, value: 0 }));
  };

  return (
    <div className="p-4 border-b">
      <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 flex items-center gap-1.5">
        <Tag className="w-3.5 h-3.5" />
        Giảm giá
      </h2>

      {/* Toggle % / VND */}
      <div className="flex rounded-lg border overflow-hidden mb-3">
        <button
          className={`flex-1 py-1.5 text-sm font-medium transition-colors ${
            discount.type === "percentage"
              ? "bg-primary text-primary-foreground"
              : "bg-card text-muted-foreground hover:bg-muted"
          }`}
          onClick={() => handleSetType("percentage")}
        >
          Phần trăm (%)
        </button>
        <button
          className={`flex-1 py-1.5 text-sm font-medium transition-colors ${
            discount.type === "fixed"
              ? "bg-primary text-primary-foreground"
              : "bg-card text-muted-foreground hover:bg-muted"
          }`}
          onClick={() => handleSetType("fixed")}
        >
          Số tiền ($)
        </button>
      </div>

      {/* Input */}
      <div className="relative">
        <Input
          type="number"
          min={0}
          max={discount.type === "percentage" ? 100 : subtotal}
          placeholder={discount.type === "percentage" ? "0 – 100" : "0"}
          value={discount.value || ""}
          onChange={handleSetValue}
          className="pr-10"
        />
        <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-muted-foreground pointer-events-none">
          {discount.type === "percentage" ? "%" : "$"}
        </span>
      </div>

      {/* Preview số tiền giảm */}
      {discountAmount > 0 && (
        <p className="mt-2 text-xs text-emerald-600 font-medium text-right">
          Tiết kiệm: {fmtVND(discountAmount)}
        </p>
      )}
    </div>
  );
};

export default DiscountSection;
