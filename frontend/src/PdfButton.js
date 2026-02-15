import React from "react";
import "./App.css";

function PdfButton({ onGenerate }) {
  return (
    <div className="card" style={{ textAlign: "center" }}>
      <button className="pdf-button" onClick={onGenerate}>
        Generate PDF Report
      </button>

      <p style={{ marginTop: "12px", fontSize: "14px", color: "#475569" }}>
        Creates a polished underwriting report using your enriched JSON.
      </p>
    </div>
  );
}

export default PdfButton;
