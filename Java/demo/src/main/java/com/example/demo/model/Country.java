package com.example.demo.model;

import java.util.Date;

import jakarta.persistence.Table;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity()
@Table(name = "standard_country_dimension")
public class Country {
    @Column(
        name = "standard_country_name"
    )
    private String countryName;
    @Id
    private String countryCode;
    private Date lastUpdated;

    public Country(){

    }
    public Country(String name, String code){
        this.countryName = name;
        this.countryCode = code;
        this.lastUpdated = new Date();
    }

    public void setName(String name){
        this.countryName = name;
    }
    public void setCode(String code){
        this.countryCode = code;
    }

    public String getCode(){
        return this.countryCode;
    }
    public String getName(){
        return this.countryName;
    }
    public Date getDate(){
        return this.lastUpdated;
    }

}
