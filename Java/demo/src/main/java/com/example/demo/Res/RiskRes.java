package com.example.demo.Res;

import java.util.ArrayList;
import java.util.List;

import com.example.demo.model.Customer;

public class RiskRes {
    public Customer customer;
    public double overallRisk;
    public List<CategoryRes> categories = new ArrayList<>();

}
