package com.example.demo.controller;

import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;

import jakarta.persistence.EntityManager;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.Res.CustomersWithRisk;
import com.example.demo.model.Commodity;
import com.example.demo.model.ComplexRisk;
import com.example.demo.model.Country;
import com.example.demo.model.Customer;
import com.example.demo.model.CustomerJson;
import com.example.demo.model.RiskCategory;
import com.example.demo.service.CommodityService;
import com.example.demo.service.ComplexRiskService;
import com.example.demo.service.CountryService;
import com.example.demo.service.CustomerService;
import com.example.demo.service.RiskCategoryService;

@RestController
@RequestMapping("/customers")
public class CustomerController {

    private final CustomerService customerService;
    private final CountryService countryService;
    private final CommodityService commodityService;
    private final ComplexRiskService complexRiskService;
    private final RiskCategoryService riskCategoryService;

    public static class RiskCategorySort implements Comparator<RiskCategory> {
        public int compare(RiskCategory a, RiskCategory b) {
            return a.getId() - b.getId();
        }
    }

    @Autowired
    public CustomerController(CustomerService customerSer, ComplexRiskService complexRisk, CountryService countryService, CommodityService commodityService, RiskCategoryService riskCatServ) {
        this.customerService = customerSer;
        this.countryService = countryService;
        this.commodityService = commodityService;
        this.complexRiskService = complexRisk;
        this.riskCategoryService = riskCatServ;
    }

    @Autowired
    private EntityManager entityManager;

    @CrossOrigin
    @GetMapping
    public CustomersWithRisk getCustomers() {
        List<Customer> customers = customerService.getCustomers();
        CustomersWithRisk customersWithRisk = new CustomersWithRisk();

        for (Customer customer : customers) {
            double overall = 0.0;
            String countryCode = customer.getImportCountry();

            // Get commodity name
            int commID = Integer.parseInt(customer.getCommodity());
            String commName = commodityService.getCommodity(commID)
                    .map(Commodity::getName)
                    .orElse("");

            // Get complex risks
            List<ComplexRisk> complexRisks = complexRiskService.getAll(countryCode, customer.getRegion(), commName);
            complexRisks.forEach(complexRisk -> this.entityManager.detach(complexRisk));
            System.out.println("Customer ID: " + customer.getCustomerId());
            System.out.println("Country = " + countryCode + "\nRegion = " + customer.getRegion() + "\nCommodity = " +commName);
            // Get and sort risk categories
            List<RiskCategory> riskCategories = riskCategoryService.getAll();
            riskCategories.sort(new RiskCategorySort());
            int complexIndex = 0;

            // Calculate overall risk
            for (RiskCategory riskCat : riskCategories) {
                double weight = riskCat.getWeight() / 100.0;
                if (complexIndex < complexRisks.size()) {
                    ComplexRisk complexRisk = complexRisks.get(complexIndex);
                    if (riskCat.getId() == complexRisk.risk_category_id) {
                        overall += weight * complexRisk.risk_score;
                        complexIndex++;
                        System.out.println();
                        System.out.println("Complex Risk = " + complexRisk.risk_score);
                        System.out.println("Weight = " + weight);
                        System.out.println("Overall = " + overall);
                    }
                }
            }

            double fin = Math.round(overall * 10) / 10.0;
            System.out.println("fin = " + fin);
            customersWithRisk.overallRisk.add(fin);
            System.out.println("Final Risk Score for Customer ID " + customer.getCustomerId() + ": " + fin);

            // Update risk score in the database
            customerService.updateRiskScore(fin, customer.getCustomerId());
            complexRisks.clear();
        }

        // Populate CustomersWithRisk with customer list
        customersWithRisk.customerList = customers;

        // Additional data processing
        for (Customer customer : customersWithRisk.customerList) {
            String countryCode = customer.getImportCountry();
            countryService.getCountry(countryCode)
                    .ifPresent(country -> customer.setImportCountry(country.getName()));

            int commodityId = Integer.parseInt(customer.getCommodity());
            commodityService.getCommodity(commodityId)
                    .ifPresent(commodity -> customer.setCommodity(commodity.getName()));
        }
        return customersWithRisk;
    }
    /*
    @CrossOrigin
    @GetMapping
    public CustomersWithRisk getCustomers() {
        List<Customer> customers = this.customerService.getCustomers();
        CustomersWithRisk customersWithRisk = new CustomersWithRisk();

        double overall;
        for (Customer customer : customers) {
            overall = 0.0;
            String countryCode = customer.getImportCountry();
//            Optional<Country> country = this.countryService.getCountry(customer.getImportCountry());
//            country.ifPresent(countr -> customer.setImportCountry(countr.getName()));
//
//            int commodityId = Integer.parseInt(customer.getCommodity());
//            Optional<Commodity> commodity = this.commodityService.getCommodity(commodityId);
//            commodity.ifPresent(commod -> customer.setCommodity(commod.getName()));

            int commId = Integer.parseInt(customer.getCommodity());
            Optional<Commodity> commod = this.commodityService.getCommodity(commId);
            String commName = "";
            if(commod.isPresent()) {
                commName = commod.get().getName();
            };

            //Individual risks
            List<ComplexRisk> complexRisks = this.complexRiskService.getAll(countryCode, customer.getRegion(), commName);
            //weights
            List<RiskCategory> riskCategories = this.riskCategoryService.getAll();
            riskCategories.sort(new RiskCategorySort());
            int complexIndex = 0;

            for (RiskCategory riskCat : riskCategories) {
                double weight = (riskCat.getWeight() * 1.0) / 100;
                if (complexIndex < complexRisks.size()) {
                    ComplexRisk complexRisk = complexRisks.get(complexIndex);
                    if (riskCat.getId() == complexRisk.risk_category_id) {
                        overall += (weight * complexRisk.risk_score);
                        complexIndex++;
                }
                }
            }
            double fin = (double) Math.round(overall * 10) / 10;
            customersWithRisk.overallRisk.add(fin);

             * The problem is at this updateRiskScore which uses a nativeQuery
             * The Query is in the customerRepoForDB ad then used in CustomerService

            //this.customerService.updateRiskScore(fin, customer.getCustomerId());
        }

        customersWithRisk.customerList = customers;

        for (Customer customer : customersWithRisk.customerList) {
            String countryCode = customer.getImportCountry();
            Optional<Country> country = this.countryService.getCountry(customer.getImportCountry());
            country.ifPresent(countr -> customer.setImportCountry(countr.getName()));

            int commodityId = Integer.parseInt(customer.getCommodity());
            Optional<Commodity> commodity = this.commodityService.getCommodity(commodityId);
            commodity.ifPresent(commod -> customer.setCommodity(commod.getName()));
        }

        return customersWithRisk;
    }
*/
    @CrossOrigin
    @PostMapping
    public void addCustomer(@RequestBody CustomerJson customerJson) {
        Customer customer = new Customer(customerJson);
        this.customerService.addCustomer(customer);
    }


}
