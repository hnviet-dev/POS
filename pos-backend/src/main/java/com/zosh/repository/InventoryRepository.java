package com.zosh.repository;

import com.zosh.modal.Inventory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface InventoryRepository extends JpaRepository<Inventory, Long> {
    Inventory findByProductId(Long productId);

    List<Inventory> findByBranchId(Long branchId);

    Optional<Inventory> findByBranchIdAndProductId(Long branchId, Long productId);

    @Query("""
                SELECT COUNT(i)
                FROM Inventory i
                JOIN i.product p
                WHERE i.branch.id = :branchId
                AND i.quantity <= 5
            """)
    int countLowStockItems(@Param("branchId") Long branchId);

    // ═══════════════════════════════════════════
    // AI CHATBOT QUERIES
    // ═══════════════════════════════════════════

    @Query("""
                SELECT p.name, b.name, i.quantity
                FROM Inventory i
                JOIN i.product p
                JOIN i.branch b
                WHERE b.store.id = :storeId
                AND i.quantity <= :threshold
                ORDER BY i.quantity ASC
            """)
    List<Object[]> findLowStockItems(@Param("storeId") Long storeId,
            @Param("threshold") int threshold);

}
