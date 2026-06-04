import React from "react";
import { Card, CardContent } from "../../../components/ui/card";
import { Badge } from "../../../components/ui/badge";
import { useDispatch, useSelector } from "react-redux";
import { useToast } from "../../../components/ui/use-toast";
import { addToCart, selectCartItems } from "../../../Redux Toolkit/features/cart/cartSlice";

// stockQuantity:
//   undefined  → sản phẩm chưa được nhập kho tại branch này
//   0          → hết hàng
//   1-5        → tồn kho thấp (cảnh báo)
//   > 5        → bình thường

const ProductCard = ({ product, stockQuantity }) => {
  const dispatch = useDispatch();
  const { toast } = useToast();
  const cartItems = useSelector(selectCartItems);

  const isNotInInventory = stockQuantity === undefined;
  const isOutOfStock = stockQuantity === 0;
  const isUnavailable = isNotInInventory || isOutOfStock;
  const isLowStock = !isUnavailable && stockQuantity <= 5;

  const handleAddToCart = () => {
    if (isUnavailable) return;

    const inCart = cartItems.find((c) => c.id === product.id);
    const currentCartQty = inCart?.quantity || 0;

    if (currentCartQty >= stockQuantity) {
      toast({
        title: "Không đủ tồn kho",
        description: `"${product.name}" chỉ còn ${stockQuantity} trong kho (đã có ${currentCartQty} trong giỏ)`,
        variant: "destructive",
        duration: 3000,
      });
      return;
    }

    dispatch(addToCart(product));
    toast({
      title: "Đã thêm vào giỏ",
      description: product.name,
      duration: 1500,
    });
  };

  const stockBadge = () => {
    if (isNotInInventory) {
      return (
        <Badge variant="outline" className="text-xs text-gray-400 border-gray-300">
          Chưa nhập kho
        </Badge>
      );
    }
    if (isOutOfStock) {
      return (
        <Badge variant="outline" className="text-xs text-red-500 border-red-300">
          Hết hàng
        </Badge>
      );
    }
    if (isLowStock) {
      return (
        <Badge variant="outline" className="text-xs text-amber-600 border-amber-400 font-semibold">
          Còn {stockQuantity}
        </Badge>
      );
    }
    return (
      <Badge variant="outline" className="text-xs text-green-600 border-green-400">
        Còn {stockQuantity}
      </Badge>
    );
  };

  return (
    <Card
      className={`transition-all duration-200 border-2 ${
        isUnavailable
          ? "opacity-50 grayscale cursor-not-allowed border-gray-200"
          : "cursor-pointer hover:shadow-md hover:border-green-700"
      }`}
      onClick={handleAddToCart}
    >
      <CardContent className="p-3">
        <div className="aspect-square bg-muted rounded-md mb-2 flex items-center justify-center overflow-hidden relative">
          <img
            className="h-24 w-24 object-cover"
            src={product.image}
            alt={product.name}
            onError={(e) => {
              e.target.style.display = "none";
              e.target.nextSibling.style.display = "flex";
            }}
          />
          {/* Fallback placeholder khi ảnh lỗi */}
          <div
            className="hidden absolute inset-0 items-center justify-center text-gray-400 text-xs"
            style={{ display: "none" }}
          >
            No image
          </div>

          {/* Badge tồn kho góc trên phải */}
          <div className="absolute top-1 right-1">{stockBadge()}</div>
        </div>

        <h3 className="font-medium text-sm truncate">{product.name}</h3>
        <p className="text-xs text-muted-foreground">{product.sku}</p>

        <div className="flex items-center justify-between mt-1">
          <span className={`font-bold text-sm ${isUnavailable ? "text-gray-400" : "text-green-600"}`}>
            {(product.sellingPrice || product.price || 0).toLocaleString("vi-VN")}₫
          </span>
          <Badge variant="secondary" className="text-xs max-w-[80px] truncate">
            {product.category?.name || product.category || ""}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProductCard;
