package com.example.demo.model;

import java.util.Date;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Id;

@Entity
@Table(name = "commodities")
public class Commodity {
    private String commodityName;
    @Id
    private int commodityId;
    private Date lastUpdated;

    public Commodity(){

    }
    public Commodity(String cN, int cI){
        this.commodityName = cN;
        this.commodityId = cI;
        this.lastUpdated = new Date();
    }

    public void setName(String name){
        this.commodityName = name;
    }
    public void setId(int id){
        this.commodityId = id;
    }
    public String getName(){
        return this.commodityName;
    }
    public int getId(){
        return this.commodityId;
    }
    public Date getDate(){
        return this.lastUpdated;
    }
    
}
