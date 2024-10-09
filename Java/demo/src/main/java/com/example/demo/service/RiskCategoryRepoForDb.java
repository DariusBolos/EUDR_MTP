package com.example.demo.service;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.RiskCategory;

public interface RiskCategoryRepoForDb extends JpaRepository<RiskCategory, Integer> {
}
