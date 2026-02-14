import React from "react";

function JsonViewer({ data }) {
  if (!data) return null;

  return (
    <pre
      style={{
        background: "#f3f4f6",
        padding: "20px",
        borderRadius: "12px",
        border: "1px solid #e5e7eb",
        maxHeight: "450px",
        overflow: "auto",
        fontSize: "14px",
        lineHeight: "1.5",
      }}
    >
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}

export default JsonViewer;
