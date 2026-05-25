package com.zosh.repository;

import com.zosh.modal.Order;
import com.zosh.modal.User;
import com.zosh.payload.StoreAnalysis.BranchSalesDTO;
import com.zosh.payload.StoreAnalysis.PaymentInsightDTO;
import com.zosh.payload.StoreAnalysis.TimeSeriesPointDTO;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerId(Long customerId);
    List<Order> findByBranchId(Long branchId);
    List<Order> findByCashierId(Long cashierId);
    List<Order> findByBranchIdAndCreatedAtBetween(Long branchId,
                                                  LocalDateTime start,
                                                  LocalDateTime end);
    List<Order> findByCashierAndCreatedAtBetween(User cashier,
                                                 LocalDateTime start,
                                                 LocalDateTime end);
    List<Order> findTop5ByBranchIdOrderByCreatedAtDesc(Long branchId);

    @Query(""" 
            SELECT SUM(o.totalAmount) 
            FROM Order o 
            WHERE o.branch.id = :branchId  
            AND o.createdAt BETWEEN :start AND :end
           """)
    Optional<BigDecimal> getTotalSalesBetween(@Param("branchId") Long branchId,
                                              @Param("start") LocalDateTime start,
                                              @Param("end") LocalDateTime end);

    @Query("""
        SELECT u.id, u.fullName, SUM(o.totalAmount) AS totalRevenue
        FROM Order o
        JOIN o.cashier u
        WHERE o.branch.id = :branchId
        GROUP BY u.id, u.fullName
        ORDER BY totalRevenue DESC
    """)
    List<Object[]> getTopCashiersByRevenue(@Param("branchId") Long branchId);

    @Query("""
        SELECT COUNT(o)
        FROM Order o
        WHERE o.branch.id = :branchId
        AND DATE(o.createdAt) = :date
    """)
    int countOrdersByBranchAndDate(@Param("branchId") Long branchId,
                                   @Param("date") LocalDate date);

    @Query("""
        SELECT COUNT(DISTINCT o.cashier.id)
        FROM Order o
        WHERE o.branch.id = :branchId
        AND DATE(o.createdAt) = :date
    """)
    int countDistinctCashiersByBranchAndDate(@Param("branchId") Long branchId,
                                             @Param("date") LocalDate date);

    @Query("""
    SELECT o.paymentType, SUM(o.totalAmount), COUNT(o)
    FROM Order o
    WHERE o.branch.id = :branchId
    AND DATE(o.createdAt) = :date
    GROUP BY o.paymentType
""")
    List<Object[]> getPaymentBreakdownByMethod(
            @Param("branchId") Long branchId,
            @Param("date") LocalDate date
    );

    ////////////////////


        @Query("SELECT SUM(o.totalAmount) FROM Order o WHERE o.branch.store.storeAdmin.id = :storeAdminId")
        Optional<Double> sumTotalSalesByStoreAdmin(@Param("storeAdminId") Long storeAdminId);

        @Query("SELECT COUNT(o) FROM Order o WHERE o.branch.store.storeAdmin.id = :storeAdminId")
        int countByStoreAdminId(@Param("storeAdminId") Long storeAdminId);
//

    @Query("""
    SELECT o FROM Order o 
    WHERE o.branch.store.storeAdmin.id = :storeAdminId 
    AND o.createdAt BETWEEN :start AND :end
""")
    List<Order> findAllByStoreAdminAndCreatedAtBetween(@Param("storeAdminId") Long storeAdminId,
                                                       @Param("start") LocalDateTime start,
                                                       @Param("end") LocalDateTime end);



    @Query("""
    SELECT new com.zosh.payload.StoreAnalysis.TimeSeriesPointDTO(
        o.createdAt,
        SUM(o.totalAmount)
    )
    FROM Order o
    WHERE o.branch.store.storeAdmin.id = :storeAdminId
     AND o.createdAt BETWEEN :start AND :end
    GROUP BY o.createdAt
    ORDER BY o.createdAt
""")
    List<TimeSeriesPointDTO> getDailySales(@Param("storeAdminId") Long storeAdminId,
                                           @Param("start") LocalDateTime start,
                                           @Param("end") LocalDateTime end);


    @Query("""
        SELECT new com.zosh.payload.StoreAnalysis.PaymentInsightDTO(
            o.paymentType,
            SUM(o.totalAmount)
        )
        FROM Order o
        WHERE o.branch.store.storeAdmin.id = :storeAdminId
        GROUP BY o.paymentType
    """)
        List<PaymentInsightDTO> getSalesByPaymentMethod(@Param("storeAdminId") Long storeAdminId);

        @Query("""
        SELECT new com.zosh.payload.StoreAnalysis.BranchSalesDTO(
            o.branch.name,
            SUM(o.totalAmount)
        )
        FROM Order o
        WHERE o.branch.store.storeAdmin.id = :storeAdminId
        GROUP BY o.branch.id
    """)
        List<BranchSalesDTO> getSalesByBranch(@Param("storeAdminId") Long storeAdminId);



    // ═══════════════════════════════════════════
    // AI CHATBOT QUERIES
    // ═══════════════════════════════════════════

    long countByBranch_Store_Id(Long storeId);

    @Query("SELECT SUM(o.totalAmount) FROM Order o WHERE o.branch.store.id = :storeId")
    Double sumTotalAmountByBranch_Store_Id(@Param("storeId") Long storeId);

    long countByBranchId(Long branchId);

    @Query("""
        SELECT COUNT(o), COALESCE(SUM(o.totalAmount), 0)
        FROM Order o
        WHERE o.branch.store.id = :storeId
        AND o.createdAt BETWEEN :start AND :end
    """)
    List<Object[]> countAndSumByStoreIdAndDateRange(
            @Param("storeId") Long storeId,
            @Param("start") LocalDateTime start,
            @Param("end") LocalDateTime end);

    @Query("""
        SELECT p.name, COUNT(oi), SUM(oi.price)
        FROM OrderItem oi
        JOIN oi.product p
        WHERE p.store.id = :storeId
        GROUP BY p.id, p.name
        ORDER BY COUNT(oi) DESC
    """)
    List<Object[]> findTopSellingProducts(@Param("storeId") Long storeId, int limit);

    @Query("""
        SELECT b.name, COUNT(o), COALESCE(SUM(o.totalAmount), 0)
        FROM Order o
        JOIN o.branch b
        WHERE b.store.id = :storeId
        GROUP BY b.id, b.name
        ORDER BY SUM(o.totalAmount) DESC
    """)
    List<Object[]> findSalesByBranchForStore(@Param("storeId") Long storeId);

//    List<Order> findByCustomerId(Long customerId);
}
