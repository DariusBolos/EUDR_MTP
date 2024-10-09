import Props from "../interfaces/props.ts";

export default function SourceBox(props: Props) {
  return (
    <div className="risk-source-card mt-4">
      <div className="risk-source-card-title">
        <h1>Risk score: {props.risk}</h1>
        <span></span>
        <div>Confidence: {props.sourceConfidence}%</div>
      </div>
      <main>
        <h6>Risk description</h6>
        <section>{props.riskDescription}</section>
        <h6>Risk source description • {props.name}</h6>
        <section>{props.sourceDescription}</section>
      </main>
    </div>
  );
}
