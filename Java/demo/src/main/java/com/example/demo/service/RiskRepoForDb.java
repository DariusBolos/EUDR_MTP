package com.example.demo.service;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.example.demo.model.Risk;
import com.example.demo.model.RiskId;
import com.example.demo.model.RiskSourcesDTO;

import java.util.List;


public interface RiskRepoForDb extends JpaRepository<Risk, RiskId> {

    public List<Risk> findAllByCountryCodeLike(String CountryCode);
}