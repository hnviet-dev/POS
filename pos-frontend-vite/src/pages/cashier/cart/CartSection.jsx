import { Button } from "@/components/ui/button";
import { ShoppingCart, Bookmark, Trash2, PackageOpen } from "lucide-react";
import CartItem from "./CartItem";
import CartSummary from "./CartSummary";
import { useSelector, useDispatch } from "react-redux";
import {
  clearCart,
  removeFromCart,
  selectCartItems,
  selectHeldOrders,
  updateCartItemQuantity,
} from "../../../Redux Toolkit/features/cart/cartSlice";
import { useToast } from "../../../components/ui/use-toast";

const CartSection = ({ setShowHeldOrdersDialog }) => {
  const cartItems = useSelector(selectCartItems);
  const heldOrders = useSelector(selectHeldOrders);
  const dispatch = useDispatch();
  const { toast } = useToast(); // ← fix bug cũ: phải destructure

  const totalUnits = cartItems.reduce((sum, i) => sum + i.quantity, 0);

  const handleUpdateCartItemQuantity = (id, newQuantity) => {
    dispatch(updateCartItemQuantity({ id, quantity: newQuantity }));
  };

  const handleRemoveFromCart = (id) => {
    dispatch(removeFromCart(id));
  };

  const handleClearCart = () => {
    dispatch(clearCart());
    toast({ title: "Đã xóa giỏ hàng", description: "Tất cả sản phẩm đã được xóa" });
  };

  return (
    <div className="w-2/5 flex flex-col bg-card border-r">
      {/* ─── Header ────────────────────────────────────────────── */}
      <div className="px-4 py-3 border-b bg-muted/50 flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-2">
          <ShoppingCart className="w-4 h-4 text-primary" />
          <span className="font-semibold text-sm text-foreground">Giỏ hàng</span>
          {cartItems.length > 0 && (
            <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-primary text-primary-foreground text-[10px] font-bold">
              {cartItems.length}
            </span>
          )}
          {totalUnits > cartItems.length && (
            <span className="text-xs text-muted-foreground">({totalUnits} sp)</span>
          )}
        </div>

        <div className="flex items-center gap-1.5">
          {/* Đơn giữ */}
          <Button
            variant="outline"
            size="sm"
            className="h-7 px-2 text-xs gap-1"
            onClick={() => setShowHeldOrdersDialog(true)}
          >
            <Bookmark className="w-3 h-3" />
            Đơn giữ
            {heldOrders.length > 0 && (
              <span className="ml-0.5 w-4 h-4 rounded-full bg-amber-500 text-white text-[9px] flex items-center justify-center font-bold">
                {heldOrders.length}
              </span>
            )}
          </Button>

          {/* Xóa giỏ */}
          {cartItems.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              className="h-7 w-7 p-0 text-muted-foreground hover:text-red-500"
              onClick={handleClearCart}
              title="Xóa giỏ hàng"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </Button>
          )}
        </div>
      </div>

      {/* ─── Danh sách sản phẩm ────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto">
        {cartItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center px-6 gap-3">
            <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
              <PackageOpen className="w-8 h-8 text-muted-foreground/50" />
            </div>
            <div>
              <p className="font-medium text-foreground">Giỏ hàng trống</p>
              <p className="text-xs text-muted-foreground mt-0.5">
                Chọn sản phẩm bên trái để thêm vào đơn
              </p>
            </div>
          </div>
        ) : (
          <div className="p-3 space-y-2">
            {cartItems.map((item) => (
              <CartItem
                key={item.id}
                item={item}
                updateCartItemQuantity={handleUpdateCartItemQuantity}
                removeFromCart={handleRemoveFromCart}
              />
            ))}
          </div>
        )}
      </div>

      {/* ─── Tổng tiền ─────────────────────────────────────────── */}
      {cartItems.length > 0 && <CartSummary />}
    </div>
  );
};

export default CartSection;
