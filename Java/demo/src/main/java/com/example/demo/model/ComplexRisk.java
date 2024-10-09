package com.example.demo.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class ComplexRisk {
    @Id
    public int rn;
    public int risk_category_id;
    public int year;
    public String country_code;
    public double risk_score;
}
