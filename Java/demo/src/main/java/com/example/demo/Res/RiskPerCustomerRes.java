package com.example.demo.Res;

import java.util.List;
import com.example.demo.model.Risk;
import com.example.demo.model.RiskCategory;

public class RiskPerCustomerRes {
    private List<Risk> risksScores;
    private List<RiskCategory> riskCategories;

    public RiskPerCustomerRes(){
        this.risksScores = null;
    }
    public RiskPerCustomerRes(List<Risk> risksScores){
        this.risksScores = risksScores;
    }

    public List<Risk> getRisksScores(){
        return this.risksScores;
    }

    public List<RiskCategory> getAllRiskCategories(){
        return this.riskCategories;
    }

    public void setRiskCategories(List<RiskCategory> riskCategories){
        this.riskCategories = riskCategories; 
    }
    public void setRisksScores(List<Risk> risksScores){
        this.risksScores = risksScores;
    }
}
