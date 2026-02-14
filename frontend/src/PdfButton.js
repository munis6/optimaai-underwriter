import React from "react";

function PdfButton({ onGenerate }) {
  return (
    <button
      onClick={onGenerate}
      style={{
        background: "linear-gradient(135deg, #2563eb, #1d4ed8)",
        color: "white",
        padding: "12px 22px",
        borderRadius: "10px",
        border: "none",
        cursor: "pointer",
        fontSize: "15px",
        fontWeight: "600",
        boxShadow: "0 4px 12px rgba(37, 99, 235, 0.3)",
        transition: "0.2s",
      }}
      onMouseOver={(e) => (e.target.style.opacity = "0.9")}
      onMouseOut={(e) => (e.target.style.opacity = "1")}
    >
      Generate PDF
    </button>
  );
}

export default PdfButton;
