import React from "react";

const getRiskLevel = (score) => {
  if (score == null) return { label: "Unknown", color: "#9ca3af" }; // gray
  if (score >= 750) return { label: "Low Risk", color: "#16a34a" }; // green
  if (score >= 600) return { label: "Medium Risk", color: "#facc15" }; // yellow
  return { label: "High Risk", color: "#dc2626" }; // red
};

const RiskPill = ({ score }) => {
  const { label, color } = getRiskLevel(score);
  return (
    <div className="risk-pill" style={{ backgroundColor: color }}>
      {label} {score != null && `(${score})`}
    </div>
  );
};


function BeforeAfterPanel({ rawJson, enrichedJson }) {
  return (
    <div className="before-after-container">
      <div className="json-panel">
        <h2>Original JSON (From Core System)</h2>
        <pre>
          {rawJson ? JSON.stringify(rawJson, null, 2) : "No JSON uploaded yet."}
        </pre>
      </div>

      <div className="json-panel">
  <h2>Enriched JSON by OptimaAI Intelligence</h2>

  {enrichedJson && (
    <RiskPill
      score={ 
        enrichedJson?.processed_data?.underwritingSummary?.riskScore ?? 
        enrichedJson?.risk_score }
    />
  )}

  <pre>
    {enrichedJson
      ? JSON.stringify(enrichedJson, null, 2)
      : "No enriched JSON available."}
  </pre>
</div>

    </div>
  );
}

export default BeforeAfterPanel;
