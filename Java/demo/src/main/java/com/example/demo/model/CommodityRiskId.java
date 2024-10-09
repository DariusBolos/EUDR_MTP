package com.example.demo.model;

import java.io.Serializable;

public class CommodityRiskId implements Serializable{
    public int year, sourceId, commodityId;
    public String countryCode; 

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

    
}
