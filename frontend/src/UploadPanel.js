import React from "react";
import "./App.css";

function UploadPanel({ onFileSelect }) {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div className="card">
      <label className="upload-label">Upload JSON File</label>

      <input
        type="file"
        accept=".json"
        className="upload-input"
        onChange={handleFileChange}
      />

      <p style={{ marginTop: "12px", fontSize: "14px", color: "#475569" }}>
        Upload a JSON file to generate your OptimaAI report.
      </p>
    </div>
  );
}

export default UploadPanel;
