package com.example.demo.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.Res.CountryCommodityRes;
import com.example.demo.model.Commodity;
import com.example.demo.model.Country;
import com.example.demo.service.CommodityService;
import com.example.demo.service.CountryService;

@RestController
public class InitController {

    private final CommodityService commodityService;
    private final CountryService countryService;

    @Autowired
    public InitController(CommodityService commoditySer, CountryService countrySer) {
        this.countryService = countrySer;
        this.commodityService = commoditySer;
    }

    @CrossOrigin
    @GetMapping(path = "/")
    public CountryCommodityRes getTheInfoForTheForm() {
        List<Country> countries = this.countryService.getAll();
        List<Commodity> commodities = this.commodityService.getAll();
        CountryCommodityRes countryCommodityRes = new CountryCommodityRes(countries, commodities);
        return countryCommodityRes;
    }
}
