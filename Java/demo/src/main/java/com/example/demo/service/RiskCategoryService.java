package com.example.demo.service;

import java.util.List;

import com.example.demo.model.UpdateRiskDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.model.RiskCategory;

@Service
public class RiskCategoryService {
    private final RiskCategoryRepoForDb riskCategoryDB;

    @Autowired
    public RiskCategoryService(RiskCategoryRepoForDb rb) {
        this.riskCategoryDB = rb;
    }

    public List<RiskCategory> getAll() {
        return this.riskCategoryDB.findAll();
    }

    public void updateWeightsByIds(List<UpdateRiskDTO> weightsToUpdate) {
        for (UpdateRiskDTO toUpdate : weightsToUpdate) {
            RiskCategory riskCategory = riskCategoryDB.findById(toUpdate.getId()).orElse(null);
            if (riskCategory != null) {
                riskCategory.setWeight(toUpdate.getNewWeight());
                riskCategoryDB.save(riskCategory);
            }
        }

    }
}
