import { Button } from "../../../components/ui/button";
import { Minus, Plus, X, Package } from "lucide-react";
import { useSelector } from "react-redux";

const CartItem = ({ item, updateCartItemQuantity, removeFromCart }) => {
  const inventories = useSelector((state) => state.inventory.inventories);
  const inventoryRecord = inventories?.find((inv) => inv.productId === item.id);
  const stockQuantity = inventoryRecord?.quantity;
  const atStockLimit = stockQuantity !== undefined && item.quantity >= stockQuantity;

  const price = item.sellingPrice || item.price || 0;
  const lineTotal = price * item.quantity;

  return (
    <div className={`flex items-center gap-2.5 rounded-lg px-3 py-2.5 border bg-background transition-colors
      ${atStockLimit ? "border-amber-200 bg-amber-50/50 dark:bg-amber-950/20" : "border-border hover:border-border/80"}`}
    >
      {/* Thumbnail / placeholder */}
      <div className="w-9 h-9 rounded-md bg-muted flex-shrink-0 overflow-hidden flex items-center justify-center">
        {item.image ? (
          <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
        ) : (
          <Package className="w-4 h-4 text-muted-foreground/40" />
        )}
      </div>

      {/* Tên + cảnh báo */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium leading-tight truncate text-foreground">{item.name}</p>
        <div className="flex items-center gap-1 mt-0.5">
          <span className="text-xs text-muted-foreground">{price.toLocaleString("vi-VN")}₫</span>
          {atStockLimit && (
            <span className="text-[10px] text-amber-600 font-medium">· tối đa {stockQuantity}</span>
          )}
        </div>
      </div>

      {/* Điều chỉnh số lượng */}
      <div className="flex items-center gap-0.5 flex-shrink-0">
        <Button
          variant="ghost"
          size="sm"
          className="h-7 w-7 p-0 rounded-full text-muted-foreground hover:text-foreground"
          onClick={() => updateCartItemQuantity(item.id, item.quantity - 1)}
        >
          <Minus className="w-3 h-3" />
        </Button>

        <span className="w-7 text-center text-sm font-bold tabular-nums select-none">
          {item.quantity}
        </span>

        <Button
          variant="ghost"
          size="sm"
          className="h-7 w-7 p-0 rounded-full text-muted-foreground hover:text-foreground"
          onClick={() => updateCartItemQuantity(item.id, item.quantity + 1)}
          disabled={atStockLimit}
          title={atStockLimit ? `Chỉ còn ${stockQuantity} trong kho` : undefined}
        >
          <Plus className={`w-3 h-3 ${atStockLimit ? "opacity-25" : ""}`} />
        </Button>
      </div>

      {/* Tổng tiền dòng */}
      <div className="w-20 text-right flex-shrink-0">
        <p className="text-sm font-bold text-primary tabular-nums">
          {lineTotal.toLocaleString("vi-VN")}₫
        </p>
      </div>

      {/* Nút xóa */}
      <Button
        variant="ghost"
        size="sm"
        className="h-6 w-6 p-0 rounded-full text-muted-foreground/40 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 flex-shrink-0"
        onClick={() => removeFromCart(item.id)}
      >
        <X className="w-3 h-3" />
      </Button>
    </div>
  );
};

export default CartItem;
