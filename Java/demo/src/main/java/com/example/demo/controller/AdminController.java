package com.example.demo.controller;

import com.example.demo.model.UpdateRiskDTO;
import com.example.demo.service.RiskCategoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/admin")
public class AdminController {
    @Autowired
    RiskCategoryService riskCategoryService;

    @CrossOrigin
    @PutMapping(path = "/weights")
    public void updateRiskCategoryWeights(@RequestBody List<UpdateRiskDTO> request) {
        riskCategoryService.updateWeightsByIds(request);
    }
}
