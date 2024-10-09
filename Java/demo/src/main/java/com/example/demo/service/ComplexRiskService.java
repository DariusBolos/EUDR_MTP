package com.example.demo.service;

import com.example.demo.model.ComplexRisk;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ComplexRiskService {
    private ComplexRiskRepoForDb complexRiskDB;

    @Autowired
    public ComplexRiskService(ComplexRiskRepoForDb db) {
        this.complexRiskDB = db;
    }

    public List<ComplexRisk> getAll(String countryCode, String region, String commodityName) {
        return this.complexRiskDB.findComplexRiskValues(countryCode, region, commodityName);
    }
}
