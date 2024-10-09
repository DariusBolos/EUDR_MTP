package com.example.demo.service;

import com.example.demo.model.RiskSourcesDTO;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface RiskWithSourcesRepoForDb extends JpaRepository<RiskSourcesDTO, Long> {
    @Query(value = """
            select foo.year,
                   scd.standard_country_name as country,
                   foo.risk_category_id,
                   rc.category_name          as category_name,
                   rc.weight                 as category_weightage,
                   foo.risk_source_id        as source_id,
                   rs.source_name            as source_name,
                   rs.confidence_percentage  as source_confidence,
                   rs.description            as source_description,
                   foo.risk_score,
                   foo.risk_description      as risk_description
            from (select risk_source_id, risk_category_id, year, country_code, risk_score, description as risk_description
                  from eudr.risks
                  where country_code =
                        (select country_code from eudr.standard_country_dimension where lower(standard_country_name) = lower(:countryName))

                  UNION
                  select risk_source_id, risk_category_id, year, country_code, risk_score, description as risk_description
                  from eudr.commodity_risks
                  where country_code =
                        (select country_code from eudr.standard_country_dimension where lower(standard_country_name) = lower(:countryName))
                    and (lower(region) = lower(:region) or region is null)

                    and commodity_id = (select commodity_id from eudr.commodities where lower(commodity_name) = lower(:commodityName))) foo
                     join eudr.risk_categories rc on foo.risk_category_id = rc.category_id
                     join eudr.risk_sources rs on foo.risk_source_id = rs.source_id
                     join eudr.standard_country_dimension scd on foo.country_code = scd.country_code
            order by foo.risk_category_id, foo.risk_source_id""",
            nativeQuery = true)
    public List<RiskSourcesDTO> getAllSources(@Param("region") String region, @Param("countryName") String countryName, @Param("commodityName") String commodityName);
}
