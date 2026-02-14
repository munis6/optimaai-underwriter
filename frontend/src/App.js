import React, { useState } from "react";
import UploadPanel from "./UploadPanel";
import JsonViewer from "./JsonViewer";
import PdfButton from "./PdfButton";

function App() {
  const [jsonData, setJsonData] = useState(null);

  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${process.env.REACT_APP_API_URL}/receive`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setJsonData(data);
  };

  const handleGeneratePdf = async () => {
    const res = await fetch(
      `${process.env.REACT_APP_API_URL}/generate-compliance-report`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsonData),
      }
    );

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "compliance_report.pdf";
    a.click();
  };

  return (
    <div
      style={{
        fontFamily: "Inter, sans-serif",
        background: "linear-gradient(135deg, #eef2f7 0%, #f9fafb 100%)",
        minHeight: "100vh",
        padding: "50px",
      }}
    >
      <div
        style={{
          maxWidth: "950px",
          margin: "0 auto",
          background: "white",
          padding: "40px",
          borderRadius: "16px",
          boxShadow: "0 8px 30px rgba(0,0,0,0.08)",
          border: "1px solid #e5e7eb",
        }}
      >
        <h1
          style={{
            marginBottom: "10px",
            fontSize: "32px",
            fontWeight: "700",
            color: "#374151",
            background: "#f3f4f6",
            padding: "12px 20px",
            borderRadius: "10px",
            border: "2px solid #000000",
          }}
        >
          OptimaAI Underwriter
        </h1>

        <p
          style={{
            color: "#374151",
            background: "#f3f4f6",
            padding: "14px 18px",
            borderRadius: "8px",
            border: "1px solid #000000",
            fontSize: "16px",
            marginBottom: "32px",
          }}
        >
          Upload your insurance JSON file, review the enriched output, and
          generate a compliance‑grade PDF report.
        </p>

        {/* UPLOAD CARD (NO HOVER ANIMATION) */}
        <div
          style={{
            marginBottom: "32px",
            padding: "24px",
            border: "2px dashed #cbd5e1",
            borderRadius: "12px",
            background: "#f8fafc",
          }}
        >
          <UploadPanel onUpload={handleUpload} />
        </div>

        {jsonData && (
          <>
            <h3
              style={{
                marginTop: "20px",
                marginBottom: "12px",
                fontSize: "20px",
                fontWeight: "600",
                color: "#374151",
              }}
            >
              Enriched JSON Output
            </h3>

            <JsonViewer data={jsonData} />

            <div style={{ marginTop: "24px" }}>
              <PdfButton onGenerate={handleGeneratePdf} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
