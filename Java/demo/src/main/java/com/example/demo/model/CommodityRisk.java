package com.example.demo.model;


import java.util.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;
import jakarta.persistence.Table;

@Entity
@Table(name = "commodity_risks")
@IdClass(CommodityRiskId.class)
public class CommodityRisk {
    public Date lastUpdated;
    @Id
    public int year;
    @Id
    public int commodityId;
    @Id
    @Column(name ="risk_source_id")
    public int sourceId;
    @Id
    public String countryCode;
    @Column(name ="risk_category_id")
    public int categoryId;
    public double riskScore;
    public String description;
    public String region;
}
