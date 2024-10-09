package com.example.demo.model;

import java.util.Date;

import jakarta.persistence.*;

@Entity
@Table(name = "risk_categories")
public class RiskCategory {
    @Id
    @Column(name = "category_id")
    private int id;

    @Column(name = "category_name")
    private String name;

    @Column(name = "last_updated")
    @Temporal(TemporalType.TIMESTAMP)
    private Date lastUpdated;

    @Column(name = "weight")
    private int weight;

    public RiskCategory() {

    }

    public RiskCategory(int weight, String name, int id) {
        this.id = id;
        this.name = name;
        this.lastUpdated = new Date();
        this.weight = weight;
    }

    @PreUpdate
    public void preUpdate() {
        this.lastUpdated = new Date();
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }

    public String getName() {
        return this.name;
    }

    public int getId() {
        return this.id;
    }

    public int getWeight() {
        return this.weight;
    }

    public Date getDate() {
        return this.lastUpdated;
    }
}
