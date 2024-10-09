package com.example.demo.model;

import java.io.Serializable;

public class RiskId implements Serializable{
    private int riskSourceId, riskCategoryId, year;
    private String countryCode;

    public RiskId(int riskSource, int riskCategory, int year, String country){
        this.countryCode = country;
        this.riskCategoryId = riskCategory;
        this.riskSourceId = riskSource;
        this.year = year;
    }

    @Override
    public boolean equals(Object obj) {
        // TODO Auto-generated method stub
        return super.equals(obj);
    }
    @Override
    public int hashCode() {
        // TODO Auto-generated method stub
        return super.hashCode();
    }
    public int getRiskSourceId(){
        return this.riskSourceId;
    }
    public int getRiskCategoryId(){
        return this.riskCategoryId;
    }
    public int getYear(){
        return this.year;
    }
    public String countryCode(){
        return this.countryCode;
    }
}
