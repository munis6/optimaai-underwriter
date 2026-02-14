import React, { useState, useRef } from "react";

function UploadPanel({ onUpload }) {
  const [fileName, setFileName] = useState("");
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      onUpload(file);
    }
  };

  const handleClear = () => {
    setFileName("");
    onUpload(null);

    // Reset the hidden file input so the same file can be uploaded again
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      {/* CHOOSE FILE BUTTON WITH HOVER LIFT */}
      <label
        style={{
          display: "inline-block",
          padding: "12px 20px",
          background: "linear-gradient(135deg, #2563eb, #1d4ed8)",
          color: "white",
          borderRadius: "10px",
          cursor: "pointer",
          fontSize: "15px",
          fontWeight: "600",
          boxShadow: "0 4px 12px rgba(37, 99, 235, 0.3)",
          transition: "0.25s ease",
          marginRight: "12px",
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.boxShadow = "0 6px 18px rgba(0,0,0,0.18)";
          e.currentTarget.style.transform = "scale(1.05)";
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.boxShadow = "0 4px 12px rgba(37,99,235,0.3)";
          e.currentTarget.style.transform = "scale(1)";
        }}
      >
        Choose File
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange}
          ref={fileInputRef}
          style={{ display: "none" }}
        />
      </label>

      {/* CLEAR BUTTON + FILE NAME */}
      {fileName && (
        <>
          <button
            onClick={handleClear}
            style={{
              padding: "10px 16px",
              background: "#ef4444",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "14px",
              fontWeight: "600",
              boxShadow: "0 3px 8px rgba(239, 68, 68, 0.3)",
              transition: "0.2s",
            }}
            onMouseOver={(e) => (e.currentTarget.style.opacity = "0.9")}
            onMouseOut={(e) => (e.currentTarget.style.opacity = "1")}
          >
            Clear
          </button>

          <div
            style={{
              marginTop: "12px",
              fontSize: "14px",
              color: "#374151",
              fontWeight: "500",
            }}
          >
            Selected: {fileName}
          </div>
        </>
      )}
    </div>
  );
}

export default UploadPanel;
