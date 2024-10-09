package com.example.demo.controller;

import com.example.demo.service.CommodityRiskService;
import com.example.demo.service.CommodityService;
import com.example.demo.service.ComplexRiskService;
import com.example.demo.service.CountryService;

import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;


import com.example.demo.Res.CategoryResWithQuery;
import com.example.demo.Res.RiskResWithQuery;
import com.example.demo.Res.SourceResWithQuery;
import com.example.demo.service.CustomerService;
import com.example.demo.service.RiskCategoryService;
import com.example.demo.service.RiskService;
import com.example.demo.service.RiskSourceService;
import com.example.demo.model.Customer;
import com.example.demo.model.Risk;
import com.example.demo.model.RiskCategory;
import com.example.demo.model.RiskSource;
import com.example.demo.model.RiskSourcesDTO;
import com.example.demo.model.Commodity;
import com.example.demo.model.ComplexRisk;
import com.example.demo.model.Country;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/customers/risks")
public class RiskController {

    private final RiskService riskService;
    private final RiskCategoryService riskCategoryService;
    private final CustomerService customerService;
    private final RiskSourceService sourceService;
    private final ComplexRiskService complexRiskService;
    private final CommodityService commodityService;
    private final CountryService countryService;
    private final CommodityRiskService commodityRiskService;

    public class RiskSort implements Comparator<Risk> {
        public int compare(Risk a, Risk b) {
            return a.getRiskCategory() - b.getRiskCategory();
        }
    }

    public class RiskCategorySort implements Comparator<RiskCategory> {
        public int compare(RiskCategory a, RiskCategory b) {
            return a.getId() - b.getId();
        }
    }

    public class SourceSort implements Comparator<RiskSource> {
        public int compare(RiskSource a, RiskSource b) {
            return a.getCatId() - b.getCatId();
        }
    }

    @Autowired
    public RiskController(RiskService riskSer, CountryService country, RiskCategoryService riskCatServ, CustomerService cust, RiskSourceService riskSourceSer, ComplexRiskService complex, CommodityService comm, CommodityRiskService commodityRiskServ) {
        this.riskService = riskSer;
        this.riskCategoryService = riskCatServ;
        this.customerService = cust;
        this.sourceService = riskSourceSer;
        this.complexRiskService = complex;
        this.commodityService = comm;
        this.countryService = country;
        this.commodityRiskService = commodityRiskServ;
    }

    @CrossOrigin
    @GetMapping(path = "{id}")
    public RiskResWithQuery getAllSources(@PathVariable(name = "id") int id) {
        RiskResWithQuery res = new RiskResWithQuery();

        // Fetch and set customer details
        Optional<Customer> customer = fetchAndSetCustomerDetails(id, res);

        // If customer is not present, return the response as is
        if (!customer.isPresent()) {
            return res;
        }

        // Extract customer details for further processing
        String region = customer.get().getRegion();
        String countryCode = customer.get().getImportCountry();
        String commodityId = customer.get().getCommodity();

        // Fetch country and commodity details
        String countryName = fetchCountryName(countryCode);
        String commodityName = fetchCommodityName(commodityId);

        // Fetch sources based on region, country, and commodity
        List<RiskSourcesDTO> sources = this.riskService.getAllSources(region, countryName, commodityName);

        // Construct the RiskRes JSON response
        constructRiskResponse(res, sources, countryCode, region, commodityName);

        return res;
    }

    private Optional<Customer> fetchAndSetCustomerDetails(int id, RiskResWithQuery res) {
        Optional<Customer> customer = this.customerService.getCustomerById(id);
        if (customer.isPresent()) {
            res.customer = customer.get();
            res.overallRisk = customer.get().getRisk();
        }
        return customer;
    }

    private String fetchCountryName(String countryCode) {
        Optional<Country> country = this.countryService.getCountry(countryCode);
        return country.map(Country::getName).orElse("");
    }

    private String fetchCommodityName(String commodityId) {
        Optional<Commodity> commodity = this.commodityService.getCommodity(Integer.parseInt(commodityId));
        return commodity.map(Commodity::getName).orElse("");
    }

    private void constructRiskResponse(RiskResWithQuery res, List<RiskSourcesDTO> sources, String countryCode, String region, String commodityName) {
        List<ComplexRisk> complexRisks = complexRiskService.getAll(countryCode, region, commodityName);
        CategoryResWithQuery category = initializeCategory(sources.get(0), complexRisks);

        for (RiskSourcesDTO source : sources) {
            // Map the source to SourceResWithQuery
            SourceResWithQuery sourceRes = mapToSourceResWithQuery(source);

            if (source.risk_category_id != category.id) {
                // Add the completed category to the response and initialize a new category
                res.categories.add(category);
                category = initializeCategory(source, complexRisks);
            }
            category.sources.add(sourceRes);
        }

        // Add the last category to the response
        res.categories.add(category);
    }

    private CategoryResWithQuery initializeCategory(RiskSourcesDTO source, List<ComplexRisk> complexRisks) {
        CategoryResWithQuery category = new CategoryResWithQuery();
        category.id = source.risk_category_id;
        category.name = source.category_name;
        category.weight = source.category_weightage;
        category.risk = getComplexRiskScore(complexRisks, category.id);
        return category;
    }

    private double getComplexRiskScore(List<ComplexRisk> complexRisks, int categoryId) {
        return complexRisks.stream()
                .filter(com -> com.risk_category_id == categoryId)
                .map(com -> com.risk_score)
                .findFirst()
                .orElse(0.0);
    }

    private SourceResWithQuery mapToSourceResWithQuery(RiskSourcesDTO source) {
        SourceResWithQuery sourceRes = new SourceResWithQuery();
        sourceRes.id = source.source_id;
        sourceRes.name = source.source_name;
        sourceRes.risk = source.risk_score;
        sourceRes.riskDescription = source.risk_description;
        sourceRes.sourceConfidence = source.source_confidence;
        sourceRes.sourceDescription = source.source_description;
        return sourceRes;
    }

}