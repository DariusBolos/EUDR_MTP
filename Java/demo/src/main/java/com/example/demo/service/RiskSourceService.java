package com.example.demo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.model.RiskSource;

@Service
public class RiskSourceService {
    private final RiskSourceRepoForDb riskSourceDB;

    @Autowired
    public RiskSourceService(RiskSourceRepoForDb rb){
        this.riskSourceDB = rb;
    }

    public List<RiskSource> getAll(){
        return this.riskSourceDB.findAll();
    }

    public Optional<RiskSource> getSource(int sourceId){
        return this.riskSourceDB.findById(sourceId);
    }
}
