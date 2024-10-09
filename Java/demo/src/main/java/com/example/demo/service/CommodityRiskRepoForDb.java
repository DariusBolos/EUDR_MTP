package com.example.demo.service;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.CommodityRisk;
import com.example.demo.model.CommodityRiskId;

public interface CommodityRiskRepoForDb extends JpaRepository<CommodityRisk, CommodityRiskId>{
    public List<CommodityRisk> findAllByCommodityIdAndCountryCodeLikeAndRegionLike(int commodityId, String countryCode, String region);

    public List<CommodityRisk> findAllByCommodityIdAndCountryCodeLike(int commodityId, String countryCode);
}
