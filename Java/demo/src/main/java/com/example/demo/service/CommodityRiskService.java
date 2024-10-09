package com.example.demo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.model.CommodityRisk;

import java.util.List;

@Service
public class CommodityRiskService {
    private final CommodityRiskRepoForDb commodityRiskDB;

    @Autowired
    public CommodityRiskService(CommodityRiskRepoForDb cm){
        this.commodityRiskDB = cm;
    }

    public List<CommodityRisk> getByCountryCodeAndRegionAndCommodityId(int commodityId, String countryCode, String region){
        return this.commodityRiskDB.findAllByCommodityIdAndCountryCodeLikeAndRegionLike(commodityId, countryCode, region);
    }

    public List<CommodityRisk> getByCommodityIdAndCountryCodeLike(int commodityId, String countryCode){
        return this.commodityRiskDB.findAllByCommodityIdAndCountryCodeLike(commodityId, countryCode);
    }
}
