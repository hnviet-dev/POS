import { BanknoteIcon, CreditCardIcon, SmartphoneIcon } from "lucide-react";

// Ánh xạ key → label tiếng Việt (dùng chung toàn hệ thống)
const PAYMENT_LABELS = {
  CASH: "Tiền mặt",
  CARD: "Thẻ ngân hàng",
  UPI:  "Chuyển khoản / QR",
};

// Icon Lucide theo loại thanh toán
export const getPaymentIcon = (method) => {
  switch (method) {
    case "CASH":
      return <BanknoteIcon   className="h-4 w-4 text-green-600" />;
    case "CARD":
      return <CreditCardIcon className="h-4 w-4 text-blue-600" />;
    case "UPI":
      return <SmartphoneIcon className="h-4 w-4 text-purple-600" />;
    default:
      return null;
  }
};

// Label tiếng Việt theo loại thanh toán
export const getPaymentLabel = (method) =>
  PAYMENT_LABELS[method] ?? method ?? "-";

/**
 * Component hiển thị icon + label đồng nhất — dùng ở mọi nơi trong hệ thống.
 * Thay thế tất cả: {getPaymentIcon(x)} {x}  →  <PaymentBadge type={x} />
 */
export const PaymentBadge = ({ type }) => (
  <div className="flex items-center gap-1.5">
    {getPaymentIcon(type)}
    <span>{getPaymentLabel(type)}</span>
  </div>
);
