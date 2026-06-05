import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Barcode, Loader2, X } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";
import ProductCard from "./ProductCard";
import { useDispatch, useSelector } from "react-redux";
import {
  getProductsByStore,
  searchProducts,
} from "../../../Redux Toolkit/features/product/productThunks";
import { getBranchById } from "../../../Redux Toolkit/features/branch/branchThunks";
import { clearSearchResults } from '@/Redux Toolkit/features/product/productSlice';
import { getInventoryByBranch } from "../../../Redux Toolkit/features/inventory/inventoryThunks";

const ProductSection = ({ searchInputRef }) => {
  const dispatch = useDispatch();
  const { branch } = useSelector((state) => state.branch);
  const { userProfile } = useSelector((state) => state.user);
  const [searchTerm, setSearchTerm] = useState("");
  const {
    products,
    searchResults,
    loading,
    error: productsError
  } = useSelector((state) => state.product);
  const { inventories } = useSelector((state) => state.inventory);

  const { toast } = useToast();

  // Map productId → quantity cho branch hiện tại
  const inventoryMap = useMemo(() => {
    const map = {};
    (inventories || []).forEach((inv) => {
      map[inv.productId] = inv.quantity;
    });
    return map;
  }, [inventories]);



  const getDisplayProducts = () => {
    if (searchTerm.trim() && searchResults.length > 0) {
      return searchResults;
    }
    return products || [];
  };

  // Fetch products + inventory khi branch thay đổi
  useEffect(() => {
    const fetchData = async () => {
      if (branch?.storeId && localStorage.getItem("jwt")) {
        try {
          await dispatch(getProductsByStore(branch.storeId)).unwrap();
        } catch (error) {
          toast({
            title: "Error",
            description: error || "Failed to fetch products",
            variant: "destructive",
          });
        }

        // Fetch inventory của branch để hiển thị tồn kho trên card
        try {
          await dispatch(getInventoryByBranch(branch.id)).unwrap();
        } catch {
          // inventory có thể chưa có — không block UI
        }
      } else if (userProfile?.branchId && localStorage.getItem("jwt") && !branch) {
        try {
          await dispatch(
            getBranchById({ id: userProfile.branchId, jwt: localStorage.getItem("jwt") })
          ).unwrap();
        } catch {
          toast({
            title: "Error",
            description: "Failed to load branch information",
            variant: "destructive",
          });
        }
      }
    };

    fetchData();
  }, [dispatch, branch, userProfile, toast]);

  // Debounced search function
  const debouncedSearch = useCallback(
    (() => {
      let timeoutId;
      return (query) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
          if (query.trim() && branch?.storeId && localStorage.getItem("jwt")) {
            dispatch(
              searchProducts({
                query: query.trim(),
                storeId: branch.storeId,
              })
            )
              .unwrap()
              .catch((error) => {
                console.error("Search failed:", error);
                toast({
                  title: "Search Error",
                  description: error || "Failed to search products",
                  variant: "destructive",
                });
              });
          }
        }, 500); // 300ms debounce
      };
    })(),
    [dispatch, branch, toast]
  );

  // Handle search term changes
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    if (e.target.value.trim()) {
      debouncedSearch(e.target.value);
    } else {
      // Clear search results when search term is empty
      dispatch(clearSearchResults());
    }
  };

  // Show error toast if products fail to load
  useEffect(() => {
    if (productsError) {
      toast({
        title: 'Error',
        description: productsError,
        variant: 'destructive',
      });
    }
  }, [productsError, toast]);

  return (
    <div className="w-2/5 flex flex-col bg-card border-r">
      {/* Search Section */}
      <div className="px-4 py-3 border-b bg-muted/50">
        <div className="relative">
          {loading ? (
            <Loader2 className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground animate-spin" />
          ) : (
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          )}
          <Input
            ref={searchInputRef}
            type="text"
            placeholder="Tìm sản phẩm hoặc quét mã (F1)"
            className="pl-9 pr-4"
            value={searchTerm}
            onChange={handleSearchChange}
            disabled={loading}
          />
          {searchTerm && (
            <button
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              onClick={() => { setSearchTerm(""); dispatch(clearSearchResults()); }}
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        <div className="flex items-center justify-between mt-2">
          <span className="text-xs text-muted-foreground">
            {loading
              ? "Đang tải..."
              : searchTerm.trim()
                ? `${getDisplayProducts().length} kết quả`
                : `${getDisplayProducts().length} sản phẩm`}
          </span>
          <Button variant="outline" size="sm" className="h-6 text-[11px] px-2" disabled={loading}>
            <Barcode className="w-3 h-3 mr-1" />
            Quét mã
          </Button>
        </div>
      </div>

      {/* Products Grid */}
      <div className="flex-1 overflow-y-auto p-3">
        {loading ? (
          <div className="grid grid-cols-3 gap-3">
            {Array.from({ length: 9 }).map((_, i) => (
              <div key={i} className="rounded-xl border bg-muted animate-pulse">
                <div className="aspect-[4/3] bg-muted-foreground/10 rounded-t-xl" />
                <div className="p-2.5 space-y-1.5">
                  <div className="h-2.5 bg-muted-foreground/10 rounded w-3/4" />
                  <div className="h-3 bg-muted-foreground/10 rounded w-1/2" />
                </div>
              </div>
            ))}
          </div>
        ) : getDisplayProducts().length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 gap-3 text-center">
            <div className="w-14 h-14 rounded-full bg-muted flex items-center justify-center">
              <Search className="w-6 h-6 text-muted-foreground/40" />
            </div>
            <div>
              <p className="font-medium text-foreground">Không tìm thấy sản phẩm</p>
              <p className="text-xs text-muted-foreground mt-0.5">
                {searchTerm ? "Thử tìm kiếm với từ khóa khác" : "Chưa có sản phẩm nào"}
              </p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-2 xl:grid-cols-3 gap-2.5">
            {getDisplayProducts().map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                stockQuantity={inventoryMap[product.id]}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductSection;
