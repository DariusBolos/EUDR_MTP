package com.example.demo.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.util.Date;

@Entity
@Table(name ="risk_sources")
public class RiskSource {
    @Id
    @Column(name ="source_id")
    private int id;
    @Column(name = "source_name")
    private String name;
    private String categoryName;
    private int categoryId;
    private String url, description;
    private Date lastUpdated;

    public RiskSource(){}
    public RiskSource(int catId, int id, String name, String url, String des, String catName){
        this.categoryId = catId;
        this.id = id;
        this.name = name;
        this.description = des;
        this.lastUpdated = new Date();
        this.categoryName = catName;
        this.url = url;

    }

    public void setId(int par){
        this.id = par;
    }
    public void setName(String par){
        this.name = par;
    }public void setCatId(int par){
        this.categoryId  =par;
    }public void setCatName(String par){
        this.categoryName = par;
    }public void setDescription(String par){
        this.description = par;
    }public void setUrl(String par){
        this.url = par;
    }

    public String getName(){
        return this.name;
    }
    public String getCatName(){
        return this.categoryName;
    }
    public int getId(){
        return this.id;
    }
    public int getCatId(){
        return this.categoryId;
    }
    public String getUrl(){
        return this.url;
    }
    public String getDescription(){
        return this.description;
    }
    public Date getLastUpdated(){
        return this.lastUpdated;
    }
}
