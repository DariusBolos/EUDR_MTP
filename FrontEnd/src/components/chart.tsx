import { Chart as ChartJS, ArcElement, Tooltip } from "chart.js";

import { useLocation } from "react-router-dom";

import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip);

interface ColorOptions {
  [key: string]: string[]; // Index signature allowing any string key to access string array values
}

function changeColorByValue(value: number) {
  const defaultColor = "darkgrey";
  //value = Math.ceil(value);
  const option = "" + value;

  const colorOptions: ColorOptions = {
    "1": [defaultColor, "green"],
    "1.1": [defaultColor, "green"],
    "1.2": [defaultColor, "green"],
    "1.3": [defaultColor, "green"],
    "1.4": [defaultColor, "green"],
    "1.5": [defaultColor, "green"],
    "1.6": [defaultColor, "green"],
    "1.7": [defaultColor, "green"],
    "1.8": [defaultColor, "green"],
    "1.9": [defaultColor, "green"],
    "2": [defaultColor, "green"],
    "2.1": [defaultColor, "green"],
    "2.2": [defaultColor, "green"],
    "2.3": [defaultColor, "green"],
    "2.4": [defaultColor, "green"],
    "2.5": [defaultColor, "#F28500"], //orange color
    "2.6": [defaultColor, "#F28500"], //orange color
    "2.7": [defaultColor, "#F28500"], //orange color
    "2.8": [defaultColor, "#F28500"], //orange color
    "2.9": [defaultColor, "#F28500"], //orange color
    "3": [defaultColor, "#F28500"], //orange color
    "3.1": [defaultColor, "#F28500"], //orange color
    "3.2": [defaultColor, "#F28500"], //orange color
    "3.3": [defaultColor, "#F28500"], //orange color
    "3.4": [defaultColor, "#F28500"], //orange color
    "3.5": [defaultColor, "#F28500"], //orange color
    "3.6": [defaultColor, "#F28500"], //orange color
    "3.7": [defaultColor, "#F28500"], //orange color
    "3.8": [defaultColor, "#F28500"], //orange color
    "3.9": [defaultColor, "#F28500"], //orange color
    "4": [defaultColor, "red"],
    "4.1": [defaultColor, "red"],
    "4.2": [defaultColor, "red"],
    "4.3": [defaultColor, "red"],
    "4.4": [defaultColor, "red"],
    "4.5": [defaultColor, "red"],
    "4.6": [defaultColor, "red"],
    "4.7": [defaultColor, "red"],
    "4.8": [defaultColor, "red"],
    "4.9": [defaultColor, "red"],
    "5": [defaultColor, "red"],
    "5.1": [defaultColor, "red"],
    "5.2": [defaultColor, "red"],
    "5.3": [defaultColor, "red"],
    "5.4": [defaultColor, "red"],
    "5.5": [defaultColor, "red"],
    "5.6": [defaultColor, "red"],
    "5.7": [defaultColor, "red"],
    "5.8": [defaultColor, "red"],
    "5.9": [defaultColor, "red"],
    "6": [defaultColor, "red"]
  };

  return colorOptions[option];
}

export default function RiskChart() {
  const { state } = useLocation();
  const item = state[0];
  const riskValue = state[1];
  const colorCombination = changeColorByValue(riskValue);
  const data = {
    datasets: [
      {
        data: [6 - riskValue, riskValue],
        backgroundColor: colorCombination,
        borderColor: "lightgrey",
      },
    ],
  };

  const options = {};

  const textCenter: any = {
    id: "textCenter",
    beforeDatasetsDraw(chart: ChartJS) {
      const { ctx, data } = chart;

      ctx.save();
      ctx.font = "bolder 35px sans-serif";
      ctx.fillStyle = colorCombination[1];
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(
        `${data.datasets[0].data[1]}`,
        chart.getDatasetMeta(0).data[1].x,
        chart.getDatasetMeta(0).data[1].y
      );
    },
  };

  return (
    <div className="chart-container">
      <h4 className="mb-4 text-center">
        Overall Risk Score for {item.customerName}
      </h4>
      <Doughnut data={data} options={options} plugins={[textCenter]}></Doughnut>
    </div>
  );
}
