import React, { useState, useEffect } from "react";
import { Button } from "../../../components/ui/button";
import { useSidebar } from "../../../context/hooks/useSidebar";
import { useSelector } from "react-redux";
import { Menu, Clock, Store } from "lucide-react";

const POSHeader = () => {
  const { setSidebarOpen } = useSidebar();
  const user = useSelector((state) => state.auth?.user || state.user?.user);
  const branchName = useSelector(
    (state) =>
      state.auth?.user?.branchName ||
      state.branch?.selectedBranch?.name ||
      null
  );

  const [time, setTime] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const timeStr = time.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  const dateStr = time.toLocaleDateString("vi-VN", { weekday: "short", day: "2-digit", month: "2-digit", year: "numeric" });

  const displayName =
    user?.fullName ||
    user?.name ||
    user?.email?.split("@")[0] ||
    "Cashier";

  return (
    <header className="bg-card border-b px-4 py-2.5 flex items-center gap-3 flex-shrink-0">
      {/* Menu button */}
      <Button
        variant="ghost"
        size="sm"
        className="h-8 w-8 p-0 flex-shrink-0"
        onClick={() => setSidebarOpen(true)}
        aria-label="Mở sidebar"
      >
        <Menu className="h-4 w-4" />
      </Button>

      {/* Brand / title */}
      <div className="flex items-center gap-1.5 flex-shrink-0">
        <div className="w-6 h-6 rounded bg-primary flex items-center justify-center">
          <Store className="w-3.5 h-3.5 text-primary-foreground" />
        </div>
        <span className="font-bold text-sm text-foreground hidden sm:block">POS Terminal</span>
      </div>

      {/* Branch name */}
      {branchName && (
        <span className="hidden md:block text-xs text-muted-foreground border-l pl-3">
          {branchName}
        </span>
      )}

      {/* Spacer */}
      <div className="flex-1" />

      {/* Đồng hồ */}
      <div className="hidden sm:flex items-center gap-1.5 text-xs text-muted-foreground">
        <Clock className="w-3.5 h-3.5 flex-shrink-0" />
        <span className="tabular-nums font-medium text-foreground">{timeStr}</span>
        <span className="text-muted-foreground/70">{dateStr}</span>
      </div>

      {/* Tên cashier */}
      {user && (
        <div className="flex items-center gap-2 border-l pl-3 ml-1 flex-shrink-0">
          <div className="w-7 h-7 rounded-full bg-primary/15 flex items-center justify-center">
            <span className="text-[11px] font-bold text-primary">
              {displayName.split(" ").map((w) => w[0]).slice(0, 2).join("").toUpperCase()}
            </span>
          </div>
          <span className="hidden md:block text-xs font-medium text-foreground max-w-[100px] truncate">
            {displayName}
          </span>
        </div>
      )}
    </header>
  );
};

export default POSHeader;
