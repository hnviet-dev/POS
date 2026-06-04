package com.zosh.service.impl;

import com.zosh.domain.OrderStatus;
import com.zosh.exception.ResourceNotFoundException;
import com.zosh.exception.UserException;
import com.zosh.modal.*;
import com.zosh.payload.dto.RefundDTO;
import com.zosh.repository.BranchRepository;
import com.zosh.repository.InventoryRepository;
import com.zosh.repository.OrderRepository;
import com.zosh.repository.RefundRepository;
import com.zosh.service.RefundService;
import com.zosh.service.UserService;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class RefundServiceImpl implements RefundService {

    private final RefundRepository refundRepository;
    private final OrderRepository orderRepository;
    private final UserService userService;
    private final BranchRepository branchRepository;
    private final InventoryRepository inventoryRepository;

    @Override
    @Transactional
    public Refund createRefund(RefundDTO refundDTO) throws UserException, ResourceNotFoundException {
        User currentCashier = userService.getCurrentUser();

        Order order = orderRepository.findById(refundDTO.getOrderId())
                .orElseThrow(() -> new ResourceNotFoundException("Order not found"));

        if (order.getStatus() == OrderStatus.REFUNDED) {
            throw new UserException("Đơn hàng này đã được hoàn tiền trước đó");
        }

        Branch branch = branchRepository.findById(refundDTO.getBranchId()).orElseThrow(
                () -> new EntityNotFoundException("Branch not found")
        );

        Refund refund = new Refund();
        refund.setOrder(order);
        refund.setCashier(currentCashier);
        refund.setReason(refundDTO.getReason());
        refund.setAmount(order.getTotalAmount());
        refund.setCreatedAt(LocalDateTime.now());
        refund.setBranch(branch);

        Refund savedRefund = refundRepository.save(refund);

        order.setStatus(OrderStatus.REFUNDED);
        orderRepository.save(order);

        // Hoàn trả tồn kho cho từng sản phẩm trong order
        if (order.getItems() != null) {
            for (OrderItem item : order.getItems()) {
                inventoryRepository
                        .findByBranchIdAndProductId(branch.getId(), item.getProduct().getId())
                        .ifPresent(inventory -> {
                            inventory.setQuantity(inventory.getQuantity() + item.getQuantity());
                            inventoryRepository.save(inventory);
                        });
            }
        }

        return savedRefund;
    }

    @Override
    public List<Refund> getAllRefunds() {
        return refundRepository.findAll();
    }

    @Override
    public List<Refund> getRefundsByCashier(Long cashierId) {
        return refundRepository.findByCashierId(cashierId);
    }

    @Override
    public List<Refund> getRefundsByShiftReport(Long shiftReportId) {
        return refundRepository.findByShiftReportId(shiftReportId);
    }

    @Override
    public List<Refund> getRefundsByCashierAndDateRange(Long cashierId, LocalDateTime from, LocalDateTime to) {
        return refundRepository.findByCashierIdAndCreatedAtBetween(cashierId, from, to);
    }

    @Override
    public List<Refund> getRefundsByBranch(Long branchId) {
        List<Refund> refunds= refundRepository.findByBranchId(branchId);
        return refunds;
    }

    @Override
    public Refund getRefundById(Long id) throws ResourceNotFoundException {
        return refundRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Refund not found"));
    }

    @Override
    public void deleteRefund(Long refundId) throws ResourceNotFoundException {
        if (!refundRepository.existsById(refundId)) {
            throw new ResourceNotFoundException("Refund not found");
        }
        refundRepository.deleteById(refundId);
    }


}
