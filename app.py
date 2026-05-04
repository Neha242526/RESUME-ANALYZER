from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "🚀 Resume Analyzer is Running!"

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Get file from request
        file = request.files.get('file')

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Save file (temporary)
        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)

        # Dummy analysis (replace later with AI)
        result = {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "analysis": "This is a sample analysis. AI integration pending."
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run app (for local testing only)
if __name__ == "__main__":
    app.run(debug=True)
