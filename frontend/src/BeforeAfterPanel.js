import React from "react";

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
