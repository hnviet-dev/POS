import DiscountSection from "./DiscountSection";
import NoteSection from "./NoteSection";
import CustomerSection from "./CustomerSection";
import PaymentSection from "./PaymentSection";

const CustomerPaymentSection = ({ setShowCustomerDialog, setShowPaymentDialog }) => {
  return (
    <div className="w-1/5 min-w-[220px] flex flex-col bg-muted/30 border-l overflow-hidden">
      {/* ─── Header ──────────────────────────────────────────── */}
      <div className="px-4 py-2.5 border-b bg-muted/60 flex-shrink-0">
        <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest">
          Thanh toán
        </p>
      </div>

      {/* ─── Scrollable content ───────────────────────────────── */}
      <div className="flex-1 overflow-y-auto flex flex-col divide-y divide-border/70">
        <CustomerSection setShowCustomerDialog={setShowCustomerDialog} />
        <DiscountSection />
        <NoteSection />
      </div>

      {/* ─── Sticky bottom: total + buttons ──────────────────── */}
      <div className="flex-shrink-0 border-t bg-card shadow-[0_-2px_8px_rgba(0,0,0,0.06)]">
        <PaymentSection setShowPaymentDialog={setShowPaymentDialog} />
      </div>
    </div>
  );
};

export default CustomerPaymentSection;
