import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Category from "../interfaces/category.ts";
import Customer from "../interfaces/customer.ts";
import SourceBox from "./source-box.tsx";

interface RiskSummaryProps {
  categoryID: number;
}

const map = {
  corruption: "Corruption",
  employee_rights: "Employee rights",
  land_use_rights: "Land use rights",
  environmental_protection: "Environmental protection",
  human_rights: "Human rights",
  deforestation_free: "Deforestation free",
  forest_degradation: "Forest degradation",
  indigenous_people: "Indigenous people",
  forest_related_regulations: "Forest related regulations",
  trade_customs_regulations: "Trade customs regulations",
  third_party_rights: "Third party rights",
};

export default function RiskSummary({ categoryID }: RiskSummaryProps) {
  const { state } = useLocation();
  const item = state[0];

  const [categories, setCategories] = useState<Category[]>([]);
  const [filteredData, setFilteredData] = useState<Category[]>([]);

  useEffect(() => {
    fetch(`http://localhost:8080/customers/risks/${item.customerId}`)
      .then((res) => res.json())
      .then((data) => {
        const { categories } = data;
        setCategories(categories);
      });
  }, []);

  useEffect(() => {
    const arr = categories.filter(
      (category: Category) => categoryID == category.id
    );
    setFilteredData(arr);
  }, [categoryID]);

  return (
    <div className="risks-container">
      {filteredData.map((category, index) => (
        <section>
          <div className="risks-container-category-title">
            <h1 key={index}>{map[category.name]}</h1>
            <span>weight = {category.weight}%</span>
          </div>
          {category.sources.map((source, index) => (
            <SourceBox
              key={index}
              name={source.name}
              riskDescription={source.riskDescription}
              sourceDescription={source.sourceDescription}
              sourceConfidence={source.sourceConfidence}
              risk={source.risk}
            />
          ))}
        </section>
      ))}
    </div>
  );
}
