// Payment methods — key phải khớp với enum PaymentType ở backend (CASH, CARD, UPI)
export const paymentMethods = [
  {
    key: "CASH",
    label: "Tiền mặt",
    icon: "💵",
    description: "Thanh toán bằng tiền mặt",
  },
  {
    key: "CARD",
    label: "Thẻ ngân hàng",
    icon: "💳",
    description: "Thẻ ATM / Visa / Mastercard",
  },
  {
    key: "UPI",
    label: "Chuyển khoản / QR",
    icon: "📲",
    description: "MoMo, VNPay, ZaloPay...",
  },
];
