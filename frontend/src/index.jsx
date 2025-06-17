import React from "react";
import ReactDOM from "react-dom/client";
import InvoiceUploader from "./pages/InvoiceUploader";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <InvoiceUploader />
  </React.StrictMode>
);