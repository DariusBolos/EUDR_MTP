import "../css/weights.css";
import { useState } from "react";

const categories = [
  "Corruption",
  "Employee rights",
  "Land use rights",
  "Environmental protection",
  "Human rights",
  "Deforestation free",
  "Forest degradation",
  "Indigenous people",
  "Forest related regulations",
  "Trade customs regulations",
  "Third party rights",
];

interface NewWeight {
  id: number;
  new_weight: number;
}

export default function WeightPage() {
  const [weights, setWeights] = useState(new Array(11).fill(undefined));
  const [success, setSuccess] = useState<boolean | undefined>(undefined);

  const handleWeightChange = (index: number, weight: number) => {
    const newInputs = [...weights];
    newInputs[index] = weight;
    setWeights(newInputs);
  };

  const sendNewWeights = () => {
    const data: NewWeight[] = [];
    let sum = 0;

    weights.forEach((element, index) => {
      if (element != undefined) {
        sum += element;
        data.push({
          id: index + 1,
          new_weight: element,
        });
      }
    });

    if (sum == 100) {
      try {
        console.log(data);
        fetch("http://localhost:8080/admin/weights", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        }).then((res) => {
          if (res.status == 200) {
            setSuccess(true);
          } else {
            setSuccess(false);
          }
        });
      } catch (err) {
        setSuccess(false);
      }
    } else {
      alert("The weights do not add up to 100");
    }
  };

  return (
    <main className="main-weights">
      {weights.map((weight, index) => (
        <section key={index} className="section-weights">
          <h1>{categories[index]}</h1>
          <span />
          <input
            type="number"
            value={weight}
            placeholder="New weight"
            onChange={(e) => {
              handleWeightChange(index, parseFloat(e.target.value));
            }}
          />
        </section>
      ))}

      <button className="submit-button-weights" onClick={sendNewWeights}>
        Apply new weights
      </button>
      {success == true && <p className="error">Updated weights successfully</p>}
      {success == false && <p className="error">Could not update weights</p>}
    </main>
  );
}
