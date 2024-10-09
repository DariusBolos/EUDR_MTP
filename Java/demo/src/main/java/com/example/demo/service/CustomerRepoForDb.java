package com.example.demo.service;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.example.demo.model.Customer;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;


public interface CustomerRepoForDb extends JpaRepository<Customer, Integer> {
    @Modifying
    @Transactional
    @Query(
            value = """
                    update eudr.customers
                    set risk_score = ?1
                    where customer_id = ?2
                    """,
            nativeQuery = true
    )
    void updateRiskForCountry(@Param("risk") double riskScore, @Param("id") int customerId);
    List<Customer> findAllByOrderByCustomerId();
}
