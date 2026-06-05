import React from "react";
import { Badge } from "../../../components/ui/badge";
import { useDispatch, useSelector } from "react-redux";
import { useToast } from "../../../components/ui/use-toast";
import { addToCart, selectCartItems } from "../../../Redux Toolkit/features/cart/cartSlice";
import { Plus, Package } from "lucide-react";
import { fmtVND } from "@/utils/formatCurrency";

// stockQuantity:
//   undefined  → chưa nhập kho tại branch
//   0          → hết hàng
//   1-5        → tồn kho thấp
//   > 5        → bình thường

const ProductCard = ({ product, stockQuantity }) => {
  const dispatch = useDispatch();
  const { toast } = useToast();
  const cartItems = useSelector(selectCartItems);

  const isNotInInventory = stockQuantity === undefined;
  const isOutOfStock = stockQuantity === 0;
  const isUnavailable = isNotInInventory || isOutOfStock;
  const isLowStock = !isUnavailable && stockQuantity <= 5;

  const inCart = cartItems.find((c) => c.id === product.id);
  const currentCartQty = inCart?.quantity || 0;
  const atCartLimit = !isUnavailable && currentCartQty >= stockQuantity;

  const handleAddToCart = () => {
    if (isUnavailable) return;

    if (atCartLimit) {
      toast({
        title: "Không đủ tồn kho",
        description: `"${product.name}" chỉ còn ${stockQuantity} trong kho`,
        variant: "destructive",
        duration: 2500,
      });
      return;
    }

    dispatch(addToCart(product));
    toast({ title: "Đã thêm vào giỏ", description: product.name, duration: 1200 });
  };

  // ── Stock badge overlay ─────────────────────────────────────────
  const StockBadge = () => {
    if (isNotInInventory)
      return <span className="bg-gray-800/70 text-white text-[10px] font-medium px-1.5 py-0.5 rounded-full">Chưa nhập kho</span>;
    if (isOutOfStock)
      return <span className="bg-red-600/90 text-white text-[10px] font-medium px-1.5 py-0.5 rounded-full">Hết hàng</span>;
    if (isLowStock)
      return <span className="bg-amber-500/90 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">Còn {stockQuantity}</span>;
    return <span className="bg-emerald-600/80 text-white text-[10px] font-medium px-1.5 py-0.5 rounded-full">Còn {stockQuantity}</span>;
  };

  // ── Cart count badge ────────────────────────────────────────────
  const CartBadge = () =>
    currentCartQty > 0 ? (
      <span className="absolute top-1.5 left-1.5 w-5 h-5 rounded-full bg-primary text-primary-foreground text-[10px] font-bold flex items-center justify-center shadow">
        {currentCartQty}
      </span>
    ) : null;

  return (
    <div
      onClick={handleAddToCart}
      className={`group relative rounded-xl overflow-hidden border bg-card transition-all duration-200 select-none
        ${isUnavailable
          ? "opacity-50 grayscale cursor-not-allowed border-border"
          : atCartLimit
            ? "cursor-pointer border-amber-300 shadow-amber-100 dark:shadow-none"
            : "cursor-pointer border-border hover:border-primary/60 hover:shadow-md hover:-translate-y-0.5"
        }`}
    >
      {/* ─── Ảnh sản phẩm ─────────────────────────────────────── */}
      <div className="relative aspect-[4/3] bg-muted overflow-hidden">
        {product.image ? (
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
            onError={(e) => { e.currentTarget.style.display = "none"; e.currentTarget.nextElementSibling.style.display = "flex"; }}
          />
        ) : null}

        {/* Placeholder khi không có ảnh */}
        <div
          className="absolute inset-0 flex flex-col items-center justify-center text-muted-foreground/40"
          style={{ display: product.image ? "none" : "flex" }}
        >
          <Package className="w-10 h-10" />
        </div>

        {/* Overlay tối khi unavailable */}
        {isUnavailable && (
          <div className="absolute inset-0 bg-background/50 flex items-center justify-center">
            <span className="text-xs font-semibold text-muted-foreground bg-background/80 px-2 py-1 rounded-full">
              {isNotInInventory ? "Chưa nhập kho" : "Hết hàng"}
            </span>
          </div>
        )}

        {/* Badge số lượng trong giỏ (góc trái) */}
        <CartBadge />

        {/* Badge tồn kho (góc phải) */}
        <div className="absolute top-1.5 right-1.5">
          <StockBadge />
        </div>

        {/* Hover overlay: nút + */}
        {!isUnavailable && (
          <div className="absolute inset-0 bg-primary/0 group-hover:bg-primary/10 transition-colors flex items-center justify-center">
            <div className="w-9 h-9 rounded-full bg-primary text-primary-foreground flex items-center justify-center shadow-lg opacity-0 group-hover:opacity-100 transition-opacity scale-75 group-hover:scale-100 duration-200">
              <Plus className="w-4 h-4" />
            </div>
          </div>
        )}
      </div>

      {/* ─── Thông tin sản phẩm ────────────────────────────────── */}
      <div className="p-2.5">
        {/* Category */}
        <p className="text-[10px] text-muted-foreground uppercase tracking-wide truncate mb-0.5">
          {product.category?.name || product.category || "—"}
        </p>

        {/* Tên */}
        <h3 className="text-sm font-semibold leading-tight truncate text-foreground">
          {product.name}
        </h3>

        {/* Giá */}
        <p className={`text-sm font-bold mt-1 ${isUnavailable ? "text-muted-foreground" : "text-primary"}`}>
          {fmtVND(product.sellingPrice || product.price || 0)}
        </p>
      </div>
    </div>
  );
};

export default ProductCard;
