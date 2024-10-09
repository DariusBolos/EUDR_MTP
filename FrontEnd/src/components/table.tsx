import Table from "react-bootstrap/Table";
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

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

export default function InformationTable() {
  const navigate = useNavigate();
  const [item, setItem] = useState<companyInformation>();

  interface companyInformation {
    customerId: number;
    customerName: string;
    customerAddress: string;
    importCountry: string;
    region: string;
    zip: string;
    commodity: string;
    yearOfTrade: string;
  }

  const [companiesInformation, setCompaniesInformation] = useState<
    companyInformation[]
  >([]);
  const [overallRisk, setOverallRisks] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8080/customers")
      .then((res) => res.json())
      .then((data) => {
        const { customerList, overallRisk } = data;
        setCompaniesInformation(customerList);
        setOverallRisks(overallRisk);
      });
  }, []);

  return (
    <div className="table-container">
      <Table hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Address</th>
            <th>Import Country</th>
            <th>Region</th>
            <th>Zip Code</th>
            <th>Commodity</th>
            <th>Year of Trade</th>
            <th>Risk Score</th>
          </tr>
        </thead>
        <tbody>
          {companiesInformation.map((item, index) => (
            <tr
              key={index}
              onClick={() => {
                setItem(item);
                navigate(`/customers/risks/${item.customerId}`, {
                  state: [item, overallRisk[index]],
                });
              }}
            >
              <td>{item.customerId}</td>
              <td>{item.customerName}</td>
              <td>{item.customerAddress}</td>
              <td>{item.importCountry}</td>
              <td>{item.region}</td>
              <td>{item.zip}</td>
              <td>{item.commodity}</td>
              <td>{item.yearOfTrade}</td>
              <td>
                <span
                  style={{
                    backgroundColor: `${changeColorByValue(
                      overallRisk[index]
                    )}`,
                  }}
                  className="risk-score-chip"
                >
                  {overallRisk[index]}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}
