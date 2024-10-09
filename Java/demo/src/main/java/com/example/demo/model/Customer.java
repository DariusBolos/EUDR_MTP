package com.example.demo.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.Date;


@Entity(name = "customers")
@Table
public class Customer {
    @Id

//    @GeneratedValue
    /*
    @SequenceGenerator(
        name="customer_id",
        sequenceName = "customer_id",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "customer_id"
    )*/

    @GeneratedValue(strategy  = GenerationType.IDENTITY)
    private int customerId;
    private String customerName, customerAddress, region, zip, commodity, importCountry;
    private int yearOfTrade;
    private Date lastUpdated;
    private double riskScore;


    public Customer(){

    }
    public Customer(String customerName, String customerAddress,String  region,
    String zip,String commodity,String importCountry, int yearOfTrade){
        this.region = region;
        this.commodity = commodity;
        this.customerAddress = customerAddress;
        this.customerName = customerName;
        this.importCountry = importCountry;
        this.lastUpdated = new Date();
        this.yearOfTrade = yearOfTrade;
        this.zip = zip;
        this.riskScore = 0.0;
    }

    public Customer(CustomerJson cj){
        this.yearOfTrade =  Integer.parseInt(cj.tradeYear);
        this.region = cj.region;
        this.commodity = cj.commodity;
        this.customerAddress = cj.customerAddress;
        this.customerName = cj.customerName;
        this.zip = cj.zip;
        this.lastUpdated = new Date();
        this.importCountry = cj.importCountry;
        this.riskScore = 0.0;
    }

    public String getCustomerName(){
        return this.customerName;
    }
    public String getCustomerAddress(){
        return this.customerAddress;
    }
    public String getZip(){
        return this.zip;
    }
    public String getRegion(){
        return this.region;
    }
    public String getCommodity(){
        return this.commodity;
    }
    public String getImportCountry(){
        return this.importCountry;
    }
    public Date getLastUpdated(){
        return this.lastUpdated;
    }
    public int getCustomerId(){
        return this.customerId;
    }
    public int getYearOfTrade(){
        return this.yearOfTrade;
    }

    public void setImportCountry(String importCountry){
        this.importCountry = importCountry;
    }

    public void setZip(String zip){
        this.zip = zip;
    }
    public void setRegion(String region){
        this.region = region;
    }
    public void setCommodity(String commodity){
        this.commodity = commodity;
    }
    public void setCustomerId(int customerId){
        this.customerId = customerId;
    }
    public void setZip(int yearOfTrade){
        this.yearOfTrade = yearOfTrade;
    }
    public void setCustomerName(String customerName){
        this.customerName = customerName;
    }
    public void setCustomerAddress(String customerAddress){
        this.customerAddress = customerAddress;
    }
    public double getRisk(){
        return this.riskScore;
    }
    public void setRisk(double riskScore){
        this.riskScore = riskScore;
    }

}
