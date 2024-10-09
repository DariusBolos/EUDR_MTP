package com.example.demo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.model.Country;

@Service
public class CountryService {
    private CountryRepoForDb countryDB;

    @Autowired
    public CountryService(CountryRepoForDb db){
        this.countryDB = db;
    }

    public List<Country> getAll(){
        return this.countryDB.findAll();
    }

    public Optional<Country> getCountry(String countryCode){
        return this.countryDB.findById(countryCode);
        
    }
}
