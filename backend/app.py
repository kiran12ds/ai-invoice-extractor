from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import openai
from openai import OpenAI
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text

def build_prompt(raw_text):
    return f"""
    You are an invoice parsing assistant. Extract the following fields from this text:
    - Vendor Name
    - Invoice Number
    - Invoice Date
    - Due Date
    - Total Amount
    - Line Items (Item Name, Quantity, Price)

    Here is the invoice text:
    {raw_text}
    """


@app.route("/api/invoice/extract", methods=["POST"])
def extract_invoice():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']

    try:
        raw_text = extract_text_from_pdf(file)
        if not raw_text.strip():
            return jsonify({"error": "No text found in the PDF"}), 400
        # Build the prompt for the OpenAI model
        if not raw_text:
            return jsonify({"error": "Empty PDF file"}), 400
        raw_text = raw_text.strip()
        if len(raw_text) > 4096:
            raw_text = raw_text[:4096]  # Truncate to fit within token limits
        # Create the prompt for the OpenAI model
        print("Received file:", file.filename)
        print("Raw text:")
        print(raw_text)

        prompt = build_prompt(raw_text)
        print("Prompt for Gemini:")
        print(prompt)
        # Call the Gemini API to extract data
        print("Calling Gemini API...")
        response = model.generate_content(prompt)
        result = response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text
        print("Response from Gemini:")
        print(result)
        return jsonify({"extracted_data": result})
    except Exception as e:
        print("Error during extraction:", str(e))
        return jsonify({"error": str(e)}), 500
        # Log the error for debugging
        # Return an error response if something goes wrong  
        raise e
        # Handle any exceptions that occur during processing


if __name__ == "__main__":
    app.run(debug=True)
