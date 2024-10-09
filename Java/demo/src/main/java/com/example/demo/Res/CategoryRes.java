package com.example.demo.Res;

import java.util.ArrayList;
import java.util.List;

public class CategoryRes {
    public int id;
    public String name;
    public double risk;
    public int weight;
    public List<SourceRes> sources = new ArrayList<>();
}
