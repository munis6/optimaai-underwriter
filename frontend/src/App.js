import React, { useState } from "react";
import "./App.css";
import UploadPanel from "./UploadPanel";
import BeforeAfterPanel from "./BeforeAfterPanel";
import PdfButton from "./PdfButton";

function App() {
  const [rawJson, setRawJson] = useState(null);
  const [isEnriching, setIsEnriching] = useState(false);
  const [riskScore, setRiskScore] = useState(null);

  const handleFileSelect = async (file) => {
    const reader = new FileReader();

    reader.onload = async (event) => {
      try {
        const parsed = JSON.parse(event.target.result);

        setRawJson(parsed);
        setIsEnriching(true);

        try {
          const result = await fetch(
            "https://optimaai-underwriter-backend.onrender.com/receive",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ data: parsed })
            }
          );

          const json = await result.json();
          setRiskScore(json.riskScore);
        } catch (err) {
          alert("Error contacting backend.");
        }

        setIsEnriching(false);
      } catch (error) {
        alert("Invalid JSON file.");
      }
    };

    reader.readAsText(file);
  };

  const handleGeneratePdf = async () => {
    if (!rawJson) {
      alert("Please upload a JSON file first.");
      return;
    }

    try {
      const response = await fetch(
        "https://optimaai-underwriter-backend.onrender.com/generate-compliance-report",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ processed_data: rawJson })
        }
      );

      if (!response.ok) {
        alert("PDF generation failed.");
        return;
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "OptimaAI_Compliance_Report.pdf";
      link.click();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert("Error generating PDF.");
    }
  };

  return (
    <div className="app-container">
      <div className="header">OptimaAI Underwriter</div>

      <UploadPanel onFileSelect={handleFileSelect} />

      {isEnriching && (
        <div className="loading-banner">Processing JSON… please wait</div>
      )}

      <BeforeAfterPanel rawJson={rawJson} riskScore={riskScore} />

      <PdfButton onGenerate={handleGeneratePdf} />
    </div>
  );
}

export default App;
