import { Card, CardContent } from "../../../components/ui/card";
import { Button } from "../../../components/ui/button";
import { Minus, Plus, Trash2 } from "lucide-react";
import { useSelector } from "react-redux";

const CartItem = ({ item, updateCartItemQuantity, removeFromCart }) => {
  const inventories = useSelector((state) => state.inventory.inventories);

  // Tìm tồn kho của sản phẩm này tại branch hiện tại
  // inventories đã được fetch theo branchId nên chỉ cần match productId
  const inventoryRecord = inventories?.find((inv) => inv.productId === item.id);
  const stockQuantity = inventoryRecord?.quantity;

  const atStockLimit =
    stockQuantity !== undefined && item.quantity >= stockQuantity;

  const price = item.sellingPrice || item.price || 0;

  return (
    <Card className="border-l-4 border-l-green-700">
      <CardContent className="p-3">
        <div className="flex items-center justify-between">
          <div className="flex-1 min-w-0 mr-2">
            <h3 className="font-medium text-sm truncate">{item.name}</h3>
            <p className="text-xs text-muted-foreground">{item.sku}</p>
            {atStockLimit && (
              <p className="text-xs text-amber-600 font-medium mt-0.5">
                Đã đạt tối đa tồn kho ({stockQuantity})
              </p>
            )}
          </div>

          <div className="flex items-center space-x-2 flex-shrink-0">
            {/* Điều chỉnh số lượng */}
            <div className="flex items-center border rounded">
              <Button
                variant="ghost"
                size="sm"
                className="h-8 w-8 p-0"
                onClick={() => updateCartItemQuantity(item.id, item.quantity - 1)}
              >
                <Minus className="w-4 h-4" />
              </Button>

              <span className="px-3 py-1 text-sm font-medium min-w-[2.5rem] text-center">
                {item.quantity}
              </span>

              <Button
                variant="ghost"
                size="sm"
                className="h-8 w-8 p-0"
                onClick={() => updateCartItemQuantity(item.id, item.quantity + 1)}
                disabled={atStockLimit}
                title={atStockLimit ? `Chỉ còn ${stockQuantity} trong kho` : undefined}
              >
                <Plus className={`w-4 h-4 ${atStockLimit ? "opacity-30" : ""}`} />
              </Button>
            </div>

            {/* Giá */}
            <div className="text-right">
              <p className="text-xs text-muted-foreground">
                {price.toLocaleString("vi-VN")}₫
              </p>
              <p className="text-sm font-bold text-green-600">
                {(price * item.quantity).toLocaleString("vi-VN")}₫
              </p>
            </div>

            {/* Xóa */}
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 p-0 text-red-500 hover:text-red-700"
              onClick={() => removeFromCart(item.id)}
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CartItem;
