package com.example.demo.service;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.RiskSource;

public interface RiskSourceRepoForDb extends JpaRepository<RiskSource, Integer> {
    
}
