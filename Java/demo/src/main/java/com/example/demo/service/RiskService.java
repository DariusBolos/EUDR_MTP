package com.example.demo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.model.Risk;
import com.example.demo.model.RiskId;
import com.example.demo.model.RiskSourcesDTO;

@Service
public class RiskService {

    @Autowired
    private final RiskRepoForDb riskUtilRepoDb;

    @Autowired
    private final RiskWithSourcesRepoForDb riskWithSourcesRepoForDb;

    public RiskService(RiskRepoForDb rb, RiskWithSourcesRepoForDb forDb) {
        this.riskUtilRepoDb = rb;
        this.riskWithSourcesRepoForDb = forDb;
    }

    public void addRisk(Risk risk) {
        this.riskUtilRepoDb.save(risk);
    }

    public List<Risk> retrieveRisks() {
        return this.riskUtilRepoDb.findAll();
    }

    public Optional<Risk> getById(RiskId id) {
        return this.riskUtilRepoDb.findById(id);
    }

    public List<Risk> getRisksByCountry(String countryCode) {
        return this.riskUtilRepoDb.findAllByCountryCodeLike(countryCode);
    }

    public List<RiskSourcesDTO> getAllSources(String region, String countryName, String commodityName) {
        return this.riskWithSourcesRepoForDb.getAllSources(region, countryName, commodityName);
    }
}

