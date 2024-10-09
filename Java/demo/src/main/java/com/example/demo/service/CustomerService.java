package com.example.demo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.model.Customer;
import java.util.List;
import java.util.Optional;

@Service
public class CustomerService {

    @Autowired
    private CustomerRepoForDb  customerUtilRepoDb;

    public CustomerService(CustomerRepoForDb cb){
        this.customerUtilRepoDb = cb;
    }
    public void addCustomer(Customer customer){
        this.customerUtilRepoDb.save(customer);
    }
    public List<Customer> getCustomers(){
        return this.customerUtilRepoDb.findAllByOrderByCustomerId();
    }
    public Optional<Customer> getCustomerById(Integer id){
        return this.customerUtilRepoDb.findById(id);
    }
    public void updateRiskScore( double riskScore, int customerId){
        this.customerUtilRepoDb.updateRiskForCountry( riskScore, customerId);
    }
}
