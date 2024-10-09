package com.example.demo.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class InfoForRiskBody {
    @JsonProperty("country_code")
    public String countryCode;
    @JsonProperty("region")
    public String region;
}
