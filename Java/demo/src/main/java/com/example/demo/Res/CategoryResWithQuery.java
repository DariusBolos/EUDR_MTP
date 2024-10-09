package com.example.demo.Res;

import java.util.ArrayList;
import java.util.List;

public class CategoryResWithQuery {
    public int id;
    public String name;
    public double risk;
    public int weight;
    public List<SourceResWithQuery> sources = new ArrayList<>();
}
