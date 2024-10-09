package com.example.demo.model;


import java.util.Date;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;
import jakarta.persistence.Table;

@Entity
@Table(name = "risks")
@IdClass(Risk.class)
public class Risk {

    @Id
    private int riskSourceId;
    @Id
    private int riskCategoryId;
    @Id
    private int year;
    @Id
    private String countryCode;
    private String description;
    private double riskScore;
    private Date last_updated;

    public Risk( int risk_source_id,
                 int risk_cat_id,
                 int year,
                 String country,
                 double risk_score){
                    
        this.countryCode = country;
        this.riskCategoryId = risk_cat_id;
        this.riskSourceId = risk_source_id;
        this.year = year;
        this.description = "";
        this.riskScore = risk_score;
        this.last_updated = new Date();
    }

    public Risk(RiskJson r){
        this.year = r.year;
        this.countryCode = r.country;
        this.riskCategoryId = r.categoryId;
        this.riskScore = r.score;
        this.description = "";
        this.riskSourceId = r.sourceId;
        this.last_updated = new Date();
    }

    public Risk(){
        this.countryCode = "Empty";
        this.riskCategoryId = 0;
        this.riskScore = 0.0;
        this.riskSourceId = 0;
        this.year = 0;
        this.description = "";
        this.last_updated = new Date();
    }

    public int getRiskSource(){
        return this.riskSourceId;

    }
    public int getRiskCategory(){
        return this.riskCategoryId;
    }
    public int getYear(){
        return this.year;
    }
    public String getCountryCode(){
        return this.countryCode;
    }
    public double getRiskScore(){
        return this.riskScore;
    }
    public Date getDate(){
        return this.last_updated;
    }
    public String getDescription(){
        return this.description;
    }
}

