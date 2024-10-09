package com.example.demo.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.model.ComplexSources;

@Service
public class ComplexSourcesService{
    private ComplexSourceRepoForDb complexSourceDB;

    @Autowired
    public ComplexSourcesService(ComplexSourceRepoForDb rs){
        this.complexSourceDB = rs;
    }

    public List<ComplexSources> getSources(String countryName, String commodityName, String region){
        return this.complexSourceDB.getSources(countryName.toLowerCase(), commodityName.toLowerCase(), region.toLowerCase());
    }
}