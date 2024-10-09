package com.example.demo.service;

import com.example.demo.model.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Objects;

@Repository
public interface ComplexRiskRepoForDb extends JpaRepository<ComplexRisk, Integer> {
    @Query(value =
            """
                            with cte as (
                            SELECT risk_category_id, sum(confidence) as total_conf
                            from
                            (
                            SELECT risk_category_id, confidence_percentage as confidence
                            FROM (SELECT r.risk_category_id, null as region, rs.confidence_percentage as confidence_percentage
                            FROM eudr.risks r left join eudr.risk_sources rs on r.risk_source_id = rs.source_id
                            WHERE lower(r.country_code) = lower(:countryCode)
                            UNION SELECT cr.risk_category_id, cr.region, rs.confidence_percentage
                            FROM eudr.commodity_risks cr left join eudr.risk_sources rs on cr.risk_source_id = rs.source_id
                            WHERE lower(cr.country_code) = lower(:countryCode)
                            AND commodity_id = (SELECT commodity_id FROM eudr.commodities WHERE lower(commodity_name) = lower(:commodityName))) foo
                            WHERE coalesce(lower(region), 'X') in (lower(:region), 'X')
                            GROUP BY risk_category_id, confidence
                            )
                            group by risk_category_id
                            )
                            SELECT row_number() OVER () as rn, risk_category_id, year, country_code, round(sum((risk_score*conf_share)),1) as risk_score
                            FROM (
                            SELECT\s
                            risk_category_id, year, country_code, round(cast(avg(risk_score) as numeric), 1) as risk_score, confidence/total_conf as conf_share
                            from
                            (
                            SELECT foo.risk_category_id as risk_category_id, year, country_code, confidence_percentage as confidence, cast(total_conf as numeric) as total_conf, round(cast(avg(risk_score) as numeric), 1) as risk_score
                            FROM (SELECT r.risk_category_id, r.year, r.country_code, null as region, rs.confidence_percentage as confidence_percentage, r.risk_score
                            FROM eudr.risks r left join eudr.risk_sources rs on r.risk_source_id = rs.source_id
                            WHERE lower(r.country_code) = lower(:countryCode)
                            UNION SELECT cr.risk_category_id as risk_category_id, cr.year, cr.country_code, cr.region, rs.confidence_percentage, cr.risk_score\s
                            FROM eudr.commodity_risks cr left join eudr.risk_sources rs on cr.risk_source_id = rs.source_id
                            WHERE lower(cr.country_code) = lower(:countryCode)
                            AND commodity_id = (SELECT commodity_id FROM eudr.commodities WHERE lower(commodity_name) = lower(:commodityName))) foo
                            join cte on foo.risk_category_id = cte.risk_category_id
                            WHERE coalesce(lower(region), 'X') in (lower(:region), 'X')
                            GROUP BY foo.risk_category_id, year, country_code, confidence, total_conf
                            )
                            GROUP BY risk_category_id, year, country_code, confidence, total_conf
                            )
                            GROUP BY risk_category_id, year, country_code
                    """,
            nativeQuery = true
    )
    public List<ComplexRisk> findComplexRiskValues(@Param("countryCode") String countryCode, @Param("region") String region, @Param("commodityName") String commodityName);
}
