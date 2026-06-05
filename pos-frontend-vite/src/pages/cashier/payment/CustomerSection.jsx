import React from "react";
import { useSelector } from "react-redux";
import { selectSelectedCustomer } from "../../../Redux Toolkit/features/cart/cartSlice";
import { User, UserCheck, ChevronRight } from "lucide-react";
import { Button } from "../../../components/ui/button";

const CustomerSection = ({ setShowCustomerDialog }) => {
  const selectedCustomer = useSelector(selectSelectedCustomer);
  const displayName = selectedCustomer?.fullName || selectedCustomer?.name;
  const initials = displayName
    ? displayName.split(" ").map((w) => w[0]).slice(0, 2).join("").toUpperCase()
    : null;

  return (
    <div className="p-4 border-b">
      <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 flex items-center gap-1.5">
        <User className="w-3.5 h-3.5" />
        Khách hàng
      </h2>

      {selectedCustomer ? (
        <button
          className="w-full flex items-center gap-3 p-2.5 rounded-lg border border-emerald-200 bg-emerald-50 dark:bg-emerald-950/40 dark:border-emerald-800 hover:bg-emerald-100 dark:hover:bg-emerald-950/60 transition-colors text-left"
          onClick={() => setShowCustomerDialog(true)}
        >
          {/* Avatar với chữ tắt */}
          <div className="w-9 h-9 rounded-full bg-emerald-500 flex items-center justify-center flex-shrink-0">
            <span className="text-white text-xs font-bold">{initials}</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-emerald-800 dark:text-emerald-200 truncate">
              {displayName}
            </p>
            <p className="text-xs text-emerald-600 dark:text-emerald-400">
              {selectedCustomer.phone || "Không có SĐT"}
            </p>
          </div>
          <ChevronRight className="w-4 h-4 text-emerald-500 flex-shrink-0" />
        </button>
      ) : (
        <Button
          variant="outline"
          className="w-full h-10 border-dashed text-muted-foreground hover:text-foreground"
          onClick={() => setShowCustomerDialog(true)}
        >
          <UserCheck className="w-4 h-4 mr-2" />
          Chọn khách hàng
        </Button>
      )}
    </div>
  );
};

export default CustomerSection;
