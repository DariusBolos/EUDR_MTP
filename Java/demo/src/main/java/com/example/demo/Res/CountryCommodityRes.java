package com.example.demo.Res;

import java.util.List;

import com.example.demo.model.Commodity;
import com.example.demo.model.Country;

public class CountryCommodityRes {
    private List<Country> countries;
    private List<Commodity> commodities;

    public CountryCommodityRes(){
        this.commodities = null;
        this.countries = null;
    }
    public CountryCommodityRes(List<Country> countries, List<Commodity> commodities){
        this.commodities = commodities;
        this.countries = countries;
    }

    public List<Country> getCountries(){
        return this.countries;
    }

    public List<Commodity> getCommodities(){
        return this.commodities;
    }

    public void setCountries(List<Country> countries){
        this.countries = countries;
    }
    public void setCommodities(List<Commodity> commodities){
        this.commodities = commodities;
    }
    
}
