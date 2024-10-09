package com.example.demo.service;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

import com.example.demo.model.ComplexSources;

public interface ComplexSourceRepoForDb extends JpaRepository<ComplexSources, Integer> {
    @Query(
            value = """
                    select foo.year, scd.standard_country_name as country, foo.risk_category_id, rc.category_name as category_name, rc.weight as category_weightage,
                    foo.risk_source_id as source_id, rs.source_name as source_name, rs.confidence_percentage as source_confidence, rs.description as source_description,
                    foo.risk_score, foo.risk_description as risk_description
                    from
                    (
                    select risk_source_id, risk_category_id, year, country_code, risk_score, description as risk_description
                    from eudr.risks 
                    where country_code = (select country_code from eudr.standard_country_dimensions where lower(standard_country_name) = :countryName)
                    UNION
                    select risk_source_id, risk_category_id, year, country_code, risk_score, description as risk_description
                    from eudr.commodity_risks
                    where country_code = (select country_code from eudr.standard_country_dimensions where lower(standard_country_name) = :countryName)
                    and (lower(region) = :region or region is null)
                    and commodity_id = (select commodity_id from eudr.commodities where lower(commodity_name) = :commodityName)
                    ) foo
                    join eudr.risk_categories rc on foo.risk_category_id = rc.category_id
                    join eudr.risk_sources rs on foo.risk_source_id = rs.source_id
                    join eudr.standard_country_dimension scd on foo.country_code = scd.country_code
                    order by foo.risk_category_id, foo.risk_source_id""",
            nativeQuery = true
    )
    public List<ComplexSources> getSources(@Param("countryName") String countryName, @Param("commodityName") String commodityName, @Param("region") String region);
}
