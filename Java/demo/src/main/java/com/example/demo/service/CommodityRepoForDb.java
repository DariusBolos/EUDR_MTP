package com.example.demo.service;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.Commodity;

public interface CommodityRepoForDb extends JpaRepository<Commodity, Integer>{

}
