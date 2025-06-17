import { useState } from "react";
import axios from "axios";

// This code defines a simple React component for uploading an invoice PDF file and extracting data from it using an AI backend service.
// It uses Axios for HTTP requests and manages state with React's useState hook.

export default function InvoiceUploader() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please upload a file first.");

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5000/api/invoice/extract", formData);
        if (response.status !== 200) {
            throw new Error("Failed to extract invoice data.");
        }
        if (response.data.extracted_data) {
            setResult(response.data.extracted_data);
        } else {
            setResult("⚠️ No data found in response.");
        }
    } catch (err) {
      setResult("Error extracting invoice data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-4 border rounded shadow">
      <h1 className="text-2xl font-bold mb-4">AI Invoice Extractor</h1>
      <input type="file" accept=".pdf" onChange={handleFileChange} className="mb-4" />
      <button onClick={handleUpload} className="bg-blue-600 text-white px-4 py-2 rounded">
        {loading ? "Processing..." : "Extract Invoice Data"}
      </button>
      {result && (
        <pre className="mt-6 whitespace-pre-wrap bg-gray-100 p-4 rounded">
          {result}
        </pre>
      )}
    </div>
  );
} 
