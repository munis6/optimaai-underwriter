import React from "react";

const getRiskLevel = (score) => {
  if (score == null) return { label: "Unknown", color: "#9ca3af" };
  if (score >= 750) return { label: "Low Risk", color: "#16a34a" };
  if (score >= 600) return { label: "Medium Risk", color: "#facc15" };
  return { label: "High Risk", color: "#dc2626" };
};

const RiskPill = ({ score }) => {
  const { label, color } = getRiskLevel(score);
  return (
    <div className="risk-pill" style={{ backgroundColor: color }}>
      {label} {score != null && `(${score})`}
    </div>
  );
};

function BeforeAfterPanel({ rawJson, riskScore }) {
  return (
    <div className="before-after-container">
      <div className="json-panel">
        <h2>Original JSON (From Core System)</h2>

        {riskScore != null && <RiskPill score={riskScore} />}

        <pre>
          {rawJson
            ? JSON.stringify(rawJson, null, 2)
            : "No JSON uploaded yet."}
        </pre>
      </div>
    </div>
  );
}

export default BeforeAfterPanel;
