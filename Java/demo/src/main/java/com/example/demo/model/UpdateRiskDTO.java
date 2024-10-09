package com.example.demo.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class UpdateRiskDTO {
    @JsonProperty("id")
    private int id;
    @JsonProperty("new_weight")
    private int newWeight;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getNewWeight() {
        return newWeight;
    }

    public void setNewWeight(int newWeight) {
        this.newWeight = newWeight;
    }
}
