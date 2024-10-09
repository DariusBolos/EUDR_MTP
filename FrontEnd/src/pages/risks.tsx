import "../css/risks.css";
import RiskChart from "../components/chart";
import RiskSummary from "../components/risk-summary.tsx";
import { useEffect, useState } from "react";
import Category from "../interfaces/category.ts";
import { useLocation } from "react-router-dom";

const all_categories = {
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

function changeColorByValue(value: number) {
  //value = Math.floor(value);
  const option = "" + value;
  const colorOptions = {
    "1": "green",
    "1.1": "green",
    "1.2": "green",
    "1.3": "green",
    "1.4": "green",
    "1.5": "green",
    "1.6": "green",
    "1.7": "green",
    "1.8": "green",
    "1.9": "green",
    "2": "green",
    "2.1": "green",
    "2.2": "green",
    "2.3": "green",
    "2.4": "green",
    "2.5": "#F28500", //orange color
    "2.6": "#F28500", //orange color
    "2.7": "#F28500", //orange color
    "2.8": "#F28500", //orange color
    "2.9": "#F28500", //orange color
    "3": "#F28500", //orange color
    "3.1": "#F28500", //orange color
    "3.2": "#F28500", //orange color
    "3.3": "#F28500", //orange color
    "3.4": "#F28500", //orange color
    "3.5": "#F28500", //orange color
    "3.6": "#F28500", //orange color
    "3.7": "#F28500", //orange color
    "3.8": "#F28500", //orange color
    "3.9": "#F28500", //orange color
    "4": "red",
    "4.1": "red",
    "4.2": "red",
    "4.3": "red",
    "4.4": "red",
    "4.5": "red",
    "4.6": "red",
    "4.7": "red",
    "4.8": "red",
    "4.9": "red",
    "5": "red",
    "5.1": "red",
    "5.2": "red",
    "5.3": "red",
    "5.4": "red",
    "5.5": "red",
    "5.6": "red",
    "5.7": "red",
    "5.8": "red",
    "5.9": "red",
    "6": "red"
  };

  return colorOptions[option];
}

export default function RiskPage() {
  const [categoryID, setCategoryID] = useState<number>(0);
  const { state } = useLocation();
  const item = state[0];

  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    fetch(`http://localhost:8080/customers/risks/${item.customerId}`)
      .then((res) => res.json())
      .then((data) => {
        const { categories } = data;
        setCategories(categories);

        console.log(categories);
      });
  }, []);

  return (
    <div className="risks-page-wrapper">
      <div className="left-section">
        <RiskChart />
        <div className="mt-4 category-selector">
          {Object.keys(all_categories).map((key, i) => {
            const index = categories.findIndex((obj) => obj.name === key);
            if (index != -1) {
              return (
                <button
                  onClick={() => {
                    setCategoryID(categories[index]?.id);
                  }}
                  style={{
                    backgroundColor: `${changeColorByValue(
                      categories[index]?.risk
                    )}`,
                  }}
                  id={`category-${i}`}
                >
                  {all_categories[categories[index].name]}
                  <span></span>
                  <p>{categories[index]?.risk}</p>
                </button>
              );
            } else {
              return <button>No data about {all_categories[key]}</button>;
            }
          })}
        </div>
      </div>
      <div className="right-section">
        <RiskSummary categoryID={categoryID} />
      </div>
    </div>
  );
}
