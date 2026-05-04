from flask import Flask, request, jsonify
import os
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI

# Load env variables
load_dotenv()

app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Home route
@app.route('/')
def home():
    return "🚀 AI Resume Analyzer Running!"

# Extract text from PDF
def extract_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Upload + Analyze
@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Save file
        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        # Extract resume text
        resume_text = extract_text(filepath)

        if not resume_text.strip():
            return jsonify({"error": "Could not extract text"}), 400

        # AI Prompt
        prompt = f"""
Analyze this resume and give:
1. ATS score (out of 100)
2. Strengths
3. Weaknesses
4. Suggestions to improve

Resume:
{resume_text}
"""

        # AI Call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        analysis = response.choices[0].message.content

        return jsonify({
            "filename": file.filename,
            "analysis": analysis
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run local
if __name__ == "__main__":
    app.run(debug=True)
