package com.example.demo.service;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.Country;

public interface CountryRepoForDb extends JpaRepository<Country, String>{

}