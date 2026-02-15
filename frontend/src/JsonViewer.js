import React from "react";
import "./App.css";

function JsonViewer({ data }) {
  if (!data) {
    return (
      <div className="card">
        <p style={{ color: "#64748b", fontSize: "15px" }}>
          No JSON loaded yet. Upload a file to view its contents.
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 style={{ marginBottom: "14px", color: "#0f766e" }}>JSON Preview</h3>

      <pre className="json-viewer">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}

export default JsonViewer;
