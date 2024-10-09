package com.example.demo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

import com.example.demo.model.Commodity;


@Service
public class CommodityService {
    private CommodityRepoForDb commodityDB;

    @Autowired
    public CommodityService(CommodityRepoForDb db){
        this.commodityDB = db;
    }

    public List<Commodity> getAll(){
        return this.commodityDB.findAll();
    }

    public Optional<Commodity> getCommodity(int id){
        return this.commodityDB.findById(id);
    }
}
