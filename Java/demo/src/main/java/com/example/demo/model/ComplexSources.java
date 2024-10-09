package com.example.demo.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class ComplexSources {
    public String country;
    @Id
    public int risk_category_id;
    public String category_name;
    public int category_weightage;
    public int source_id;
    public String source_name;
    public int source_confidence;
    public String source_description;
    public double risk_score;
    public String risk_description;
    public int year;
}
