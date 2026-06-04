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
        } catch (error) {
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
      <div className="p-4 border-b bg-muted">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <Input
            ref={searchInputRef}
            type="text"
            placeholder="Search products or scan barcode (F1)"
            className="pl-10 pr-4 py-3 text-lg"
            value={searchTerm}
            onChange={handleSearchChange}
            disabled={loading}
          />
        </div>
        <div className="flex items-center justify-between mt-2">
          <span className="text-sm text-muted-foreground">
            {loading
              ? "Loading products..."
              : searchTerm.trim()
                ? `Search results: ${getDisplayProducts().length} products found`
                : `${getDisplayProducts().length} products found`}
          </span>
          <div className="flex gap-2">
            {searchTerm.trim() && (
              <Button
                variant="ghost"
                size="sm"
                className="text-xs"
                onClick={() => setSearchTerm("")}
                disabled={loading}
              >
                <X className="w-4 h-4 mr-1" />
                Clear
              </Button>
            )}
            <Button
              variant="outline"
              size="sm"
              className="text-xs"
              disabled={loading}
            >
              <Barcode className="w-4 h-4 mr-1" />
              Scan
            </Button>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="flex-1 overflow-y-auto p-4">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="flex flex-col items-center space-y-4">
              <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
              <p className="text-muted-foreground">Loading products...</p>
            </div>
          </div>
        ) : getDisplayProducts().length === 0 ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Search className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">
                {searchTerm
                  ? "No products found matching your search"
                  : "No products available"}
              </p>
            </div>
          </div>
        ) : (
          <div className="grid lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-3">
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
