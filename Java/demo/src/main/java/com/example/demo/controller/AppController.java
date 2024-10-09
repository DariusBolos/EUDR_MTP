package com.example.demo.controller;

import java.util.List;
// import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.model.Risk;
import com.example.demo.model.RiskJson;
import com.example.demo.service.RiskService;
import com.example.demo.service.CommodityService;
import com.example.demo.service.CountryService;
import com.example.demo.service.CustomerService;


@RestController
public class AppController {

    private final RiskService riskService;
    

    @Autowired
    public AppController(RiskService rs, CustomerService cs, CountryService countrys, CommodityService coms) {
        this.riskService = rs;
        
    }


    @PostMapping(path = "/risk")
    public void addRisk(@RequestBody RiskJson riskAddedObject) {
       
        Risk res = new Risk(riskAddedObject);
        System.out.println(res.getRiskSource());
        this.riskService.addRisk(res);
    }

    @GetMapping(path = "/risk")
    public List<Risk> getRisk() {
        return this.riskService.getRisksByCountry("HU");
    }

}
