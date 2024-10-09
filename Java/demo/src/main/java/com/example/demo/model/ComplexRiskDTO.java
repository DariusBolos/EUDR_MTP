package com.example.demo.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ComplexRiskDTO {
    @JsonProperty("country_code")
    public String countryCode;
    @JsonProperty("region")
    public String region;
    @JsonProperty("commodity_name")
    public String commodityName;

    public String getCountryCode() {
        return countryCode;
    }

    public void setCountryCode(String countryCode) {
        this.countryCode = countryCode;
    }

    public String getRegion() {
        return region;
    }

    public void setRegion(String region) {
        this.region = region;
    }

    public String getCommodityName() {
        return commodityName;
    }

    public void setCommodityName(String commodityName) {
        this.commodityName = commodityName;
    }
}
